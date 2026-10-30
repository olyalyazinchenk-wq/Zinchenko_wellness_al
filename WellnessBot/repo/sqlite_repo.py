from __future__ import annotations

import contextlib
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Any, Iterator

from .base import CaseRepository


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS cases(
    submission_id TEXT PRIMARY KEY,
    user_id INTEGER,
    product_code TEXT,
    status TEXT,
    created_at TEXT,
    updated_at TEXT,
    payload_json TEXT
);

CREATE TABLE IF NOT EXISTS intake(
    submission_id TEXT PRIMARY KEY REFERENCES cases(submission_id),
    schema_version INT,
    data_json TEXT
);

CREATE TABLE IF NOT EXISTS reviews(
    id INTEGER PRIMARY KEY,
    submission_id TEXT REFERENCES cases(submission_id),
    reviewer_id INT,
    decision TEXT,
    decided_at TEXT,
    artifact_sha256 TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS payments(
    id INTEGER PRIMARY KEY,
    submission_id TEXT,
    amount_rub INT,
    mode TEXT,
    status TEXT,
    at TEXT
);

CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY,
    at TEXT,
    actor_id INT,
    submission_id TEXT,
    kind TEXT,
    data_json TEXT
);

CREATE TABLE IF NOT EXISTS sessions(
    user_id INTEGER PRIMARY KEY,
    state TEXT,
    data_json TEXT,
    updated_at TEXT
);

CREATE INDEX IF NOT EXISTS ix_cases_user ON cases(user_id);
CREATE INDEX IF NOT EXISTS ix_cases_status ON cases(status);

CREATE TRIGGER IF NOT EXISTS trg_reviews_no_update
BEFORE UPDATE ON reviews
BEGIN
    SELECT RAISE(ABORT, 'reviews table is append-only');
END;

CREATE TRIGGER IF NOT EXISTS trg_reviews_no_delete
BEFORE DELETE ON reviews
BEGIN
    SELECT RAISE(ABORT, 'reviews table is append-only');
END;
"""


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _extract_user_id(payload: dict[str, Any], submission_id: str) -> int:
    profile = payload.get("profile") if isinstance(payload.get("profile"), dict) else {}
    raw_uid = profile.get("telegram_user_id") or payload.get("user_id") or payload.get("telegram_user_id")
    if raw_uid is not None:
        try:
            return int(raw_uid)
        except (TypeError, ValueError):
            pass
    if "_" in submission_id:
        suffix = submission_id.rsplit("_", 1)[-1]
        if suffix.isdigit():
            return int(suffix)
    return 0


def _extract_product_code(payload: dict[str, Any]) -> str:
    intake = payload.get("intake") if isinstance(payload.get("intake"), dict) else {}
    raw_code = (
        payload.get("product_code")
        or intake.get("product_code")
        or payload.get("offer")
        or payload.get("tier")
        or "ok_review"
    )
    return str(raw_code).strip() or "ok_review"


def _extract_status(payload: dict[str, Any]) -> str:
    return str(
        payload.get("intake_status")
        or payload.get("status")
        or "draft"
    ).strip()


class SqliteRepository(CaseRepository):
    """SQLite implementation of CaseRepository with WAL and append-only reviews."""

    _initialized_paths: set[str] = set()

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self._ensure_initialized()

    @contextlib.contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path), timeout=15.0)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA foreign_keys = ON;")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _ensure_initialized(self) -> None:
        resolved = str(self.db_path.resolve())
        if resolved in self._initialized_paths and self.db_path.exists():
            return
        with self._connect() as conn:
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute("PRAGMA user_version = 1;")
            conn.executescript(SCHEMA_SQL)
        self._initialized_paths.add(resolved)

    def get_pragmas(self) -> dict[str, Any]:
        self._ensure_initialized()
        with self._connect() as conn:
            journal_mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
            foreign_keys = conn.execute("PRAGMA foreign_keys;").fetchone()[0]
            user_version = conn.execute("PRAGMA user_version;").fetchone()[0]
        return {
            "journal_mode": str(journal_mode).lower(),
            "foreign_keys": int(foreign_keys),
            "user_version": int(user_version),
        }

    def save_case(self, submission_id: str, payload: dict[str, Any]) -> None:
        self._ensure_initialized()
        data = dict(payload)
        data.setdefault("submission_id", submission_id)
        now_iso = _utc_now_iso()
        user_id = _extract_user_id(data, submission_id)
        product_code = _extract_product_code(data)
        status = _extract_status(data)
        created_at = str(data.get("created_at") or now_iso)
        updated_at = str(
            data.get("status_updated_at")
            or data.get("updated_at")
            or created_at
        )
        payload_json = json.dumps(data, ensure_ascii=False, sort_keys=True)

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO cases(submission_id, user_id, product_code, status, created_at, updated_at, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(submission_id) DO UPDATE SET
                    user_id = excluded.user_id,
                    product_code = excluded.product_code,
                    status = excluded.status,
                    created_at = excluded.created_at,
                    updated_at = excluded.updated_at,
                    payload_json = excluded.payload_json
                """,
                (submission_id, user_id, product_code, status, created_at, updated_at, payload_json),
            )

            intake_data = data.get("intake")
            if isinstance(intake_data, dict):
                schema_version = int(intake_data.get("schema_version") or 1)
                intake_json = json.dumps(intake_data, ensure_ascii=False, sort_keys=True)
                conn.execute(
                    """
                    INSERT INTO intake(submission_id, schema_version, data_json)
                    VALUES (?, ?, ?)
                    ON CONFLICT(submission_id) DO UPDATE SET
                        schema_version = excluded.schema_version,
                        data_json = excluded.data_json
                    """,
                    (submission_id, schema_version, intake_json),
                )

            review_records = data.get("review_records")
            if isinstance(review_records, list):
                for rec in review_records:
                    if not isinstance(rec, dict):
                        continue
                    reviewer_id = int(rec.get("reviewer_id") or 0)
                    decision = str(rec.get("decision") or "").strip()
                    decided_at = str(rec.get("decided_at") or now_iso).strip()
                    sha = str(rec.get("artifact_sha256") or "").strip()
                    notes = str(rec.get("notes") or "").strip()
                    if not decision:
                        continue
                    existing = conn.execute(
                        """
                        SELECT id FROM reviews
                        WHERE submission_id = ? AND reviewer_id = ? AND decision = ? AND decided_at = ? AND artifact_sha256 = ?
                        LIMIT 1
                        """,
                        (submission_id, reviewer_id, decision, decided_at, sha),
                    ).fetchone()
                    if existing is None:
                        conn.execute(
                            """
                            INSERT INTO reviews(submission_id, reviewer_id, decision, decided_at, artifact_sha256, notes)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """,
                            (submission_id, reviewer_id, decision, decided_at, sha, notes),
                        )

            audit_events = data.get("audit_events")
            if isinstance(audit_events, list):
                for evt in audit_events:
                    if not isinstance(evt, dict):
                        continue
                    evt_at = str(evt.get("at") or now_iso)
                    actor_id = int(evt.get("actor_id") or 0)
                    kind = str(evt.get("kind") or "event")
                    evt_data_json = json.dumps(evt.get("data") or {}, ensure_ascii=False, sort_keys=True)
                    existing_evt = conn.execute(
                        """
                        SELECT id FROM events
                        WHERE submission_id = ? AND actor_id = ? AND kind = ? AND at = ?
                        LIMIT 1
                        """,
                        (submission_id, actor_id, kind, evt_at),
                    ).fetchone()
                    if existing_evt is None:
                        conn.execute(
                            """
                            INSERT INTO events(at, actor_id, submission_id, kind, data_json)
                            VALUES (?, ?, ?, ?, ?)
                            """,
                            (evt_at, actor_id, submission_id, kind, evt_data_json),
                        )

            payment_status = str(data.get("payment_status") or "").strip()
            if payment_status:
                amount_rub = int(data.get("payment_amount_rub") or data.get("price_rub") or 0)
                mode = str(data.get("payment_mode") or "manual")
                pay_at = str(data.get("payment_confirmed_at") or data.get("payment_requested_at") or updated_at)
                existing_pay = conn.execute(
                    """
                    SELECT id FROM payments
                    WHERE submission_id = ? AND status = ? AND at = ?
                    LIMIT 1
                    """,
                    (submission_id, payment_status, pay_at),
                ).fetchone()
                if existing_pay is None:
                    conn.execute(
                        """
                        INSERT INTO payments(submission_id, amount_rub, mode, status, at)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (submission_id, amount_rub, mode, payment_status, pay_at),
                    )

    def get_case(self, submission_id: str) -> dict[str, Any] | None:
        self._ensure_initialized()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT payload_json FROM cases WHERE submission_id = ?",
                (submission_id,),
            ).fetchone()
        if row is None:
            return None
        try:
            return json.loads(row["payload_json"])
        except (json.JSONDecodeError, TypeError):
            return None

    def list_cases(
        self,
        *,
        user_id: int | None = None,
        status: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        self._ensure_initialized()
        clauses: list[str] = []
        params: list[Any] = []
        if user_id is not None:
            clauses.append("user_id = ?")
            params.append(int(user_id))
        if status is not None:
            clauses.append("status = ?")
            params.append(str(status))

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        limit_sql = f"LIMIT {int(limit)}" if limit is not None and int(limit) > 0 else ""

        query = f"""
            SELECT payload_json FROM cases
            {where_sql}
            ORDER BY updated_at DESC, created_at DESC, submission_id DESC
            {limit_sql}
        """
        results: list[dict[str, Any]] = []
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        for row in rows:
            try:
                results.append(json.loads(row["payload_json"]))
            except (json.JSONDecodeError, TypeError):
                continue
        return results

    def count_cases(self) -> int:
        self._ensure_initialized()
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS cnt FROM cases").fetchone()
        return int(row["cnt"]) if row else 0

    def append_review(
        self,
        submission_id: str,
        *,
        reviewer_id: int,
        decision: str,
        decided_at: str,
        artifact_sha256: str = "",
        notes: str = "",
    ) -> int:
        self._ensure_initialized()
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO reviews(submission_id, reviewer_id, decision, decided_at, artifact_sha256, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    submission_id,
                    int(reviewer_id),
                    str(decision),
                    str(decided_at),
                    str(artifact_sha256),
                    str(notes),
                ),
            )
            return int(cursor.lastrowid or 0)

    def list_reviews(self, submission_id: str) -> list[dict[str, Any]]:
        self._ensure_initialized()
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, submission_id, reviewer_id, decision, decided_at, artifact_sha256, notes
                FROM reviews
                WHERE submission_id = ?
                ORDER BY id ASC
                """,
                (submission_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def append_payment(
        self,
        submission_id: str,
        *,
        amount_rub: int,
        mode: str,
        status: str,
        at: str,
    ) -> int:
        self._ensure_initialized()
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO payments(submission_id, amount_rub, mode, status, at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (submission_id, int(amount_rub), str(mode), str(status), str(at)),
            )
            return int(cursor.lastrowid or 0)

    def append_event(
        self,
        *,
        actor_id: int,
        submission_id: str | None,
        kind: str,
        data: dict[str, Any] | None = None,
        at: str | None = None,
    ) -> int:
        self._ensure_initialized()
        now_iso = str(at or _utc_now_iso())
        data_json = json.dumps(data or {}, ensure_ascii=False, sort_keys=True)
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO events(at, actor_id, submission_id, kind, data_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (now_iso, int(actor_id), submission_id, str(kind), data_json),
            )
            return int(cursor.lastrowid or 0)

    def save_sessions(
        self,
        user_sessions: dict[int, dict[str, Any]],
        chat_sessions: dict[int, list[dict[str, str]]],
    ) -> None:
        self._ensure_initialized()
        now_iso = _utc_now_iso()
        all_uids: set[int] = set()
        for k in user_sessions:
            try:
                all_uids.add(int(k))
            except (TypeError, ValueError):
                continue
        for k in chat_sessions:
            try:
                all_uids.add(int(k))
            except (TypeError, ValueError):
                continue

        with self._connect() as conn:
            if not all_uids:
                conn.execute("DELETE FROM sessions")
            else:
                placeholders = ",".join("?" for _ in all_uids)
                conn.execute(f"DELETE FROM sessions WHERE user_id NOT IN ({placeholders})", list(all_uids))
            for uid in sorted(all_uids):
                u_sess = user_sessions.get(uid) or user_sessions.get(str(uid)) or {}  # type: ignore[arg-type]
                c_sess = chat_sessions.get(uid) or chat_sessions.get(str(uid)) or []  # type: ignore[arg-type]
                state = str(
                    u_sess.get("step")
                    or u_sess.get("state")
                    or u_sess.get("mode")
                    or ("chat" if c_sess else "idle")
                )
                combined = {
                    "user_session": u_sess,
                    "chat_session": c_sess,
                }
                conn.execute(
                    """
                    INSERT INTO sessions(user_id, state, data_json, updated_at)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        state = excluded.state,
                        data_json = excluded.data_json,
                        updated_at = excluded.updated_at
                    """,
                    (uid, state, json.dumps(combined, ensure_ascii=False), now_iso),
                )

    def load_sessions(self) -> dict[str, Any]:
        self._ensure_initialized()
        user_sessions: dict[str, Any] = {}
        chat_sessions: dict[str, Any] = {}
        with self._connect() as conn:
            rows = conn.execute("SELECT user_id, data_json FROM sessions ORDER BY user_id ASC").fetchall()
        for row in rows:
            uid_str = str(row["user_id"])
            try:
                parsed = json.loads(row["data_json"])
            except (json.JSONDecodeError, TypeError):
                continue
            if isinstance(parsed, dict):
                if parsed.get("user_session"):
                    user_sessions[uid_str] = parsed["user_session"]
                if parsed.get("chat_session"):
                    chat_sessions[uid_str] = parsed["chat_session"]
        return {
            "user_sessions": user_sessions,
            "chat_sessions": chat_sessions,
        }


def get_default_sqlite_repo(data_dir: Path | None = None) -> SqliteRepository:
    if data_dir is None:
        data_dir = Path(__file__).resolve().parent.parent / "data"
    return SqliteRepository(Path(data_dir) / "nutriok.db")
