from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from config import load_settings
from storage import (
    load_product_governance,
    load_product_insights,
    save_product_governance,
    save_product_insights,
)

settings = load_settings()
MOSCOW_TZ = timezone(timedelta(hours=3))
UTC_TZ = timezone.utc
PRODUCT_INSIGHT_SECTION_LABELS = [
    ("market_value_risks", "Риски ценности"),
    ("demand_risks", "Риски спроса"),
    ("value_gaps", "Провалы ценности"),
    ("positioning_upgrades", "Усиление позиционирования"),
    ("conversion_ideas", "Идеи конверсии"),
    ("retention_ideas", "Идеи удержания"),
    ("referral_ideas", "Идеи рекомендаций"),
    ("next_experiments", "Следующие эксперименты"),
]
GOVERNANCE_EXPERIMENT_STATUSES = ("proposed", "active", "validated", "rejected")


def utc_now_iso() -> str:
    return datetime.now(UTC_TZ).strftime("%Y-%m-%dT%H:%M:%SZ")


def strip_json_code_fences(raw_text: str) -> str:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def load_report_dict(report_text: str | None) -> dict[str, Any]:
    if not report_text:
        return {}
    try:
        payload = json.loads(strip_json_code_fences(report_text))
    except (json.JSONDecodeError, TypeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def clean_insight_items(items: Any) -> list[str]:
    if not isinstance(items, list):
        return []
    cleaned: list[str] = []
    for item in items:
        text = " ".join(str(item).split()).strip()
        if text:
            cleaned.append(text[:400])
    return cleaned


def normalize_insight_key(text: str) -> str:
    normalized = " ".join(text.lower().split())
    normalized = re.sub(r"[^\w\sа-яА-ЯёЁ-]", "", normalized)
    return normalized.strip()


def build_product_insights_case_snapshot(
    submission: dict[str, Any],
    judge_report_text: str | None,
    growth_report_text: str | None,
) -> dict[str, Any]:
    judge = load_report_dict(judge_report_text)
    growth = load_report_dict(growth_report_text)
    internal_review = submission.get("internal_review") or {}
    sections = {
        "market_value_risks": clean_insight_items(judge.get("market_value_risks")),
        "demand_risks": clean_insight_items(growth.get("demand_risks")),
        "value_gaps": clean_insight_items(growth.get("value_gaps")),
        "positioning_upgrades": clean_insight_items(growth.get("positioning_upgrades")),
        "conversion_ideas": clean_insight_items(growth.get("conversion_ideas")),
        "retention_ideas": clean_insight_items(growth.get("retention_ideas")),
        "referral_ideas": clean_insight_items(growth.get("referral_ideas")),
        "next_experiments": clean_insight_items(growth.get("next_experiments")),
    }
    return {
        "submission_id": submission["submission_id"],
        "captured_at": utc_now_iso(),
        "judge_verdict": internal_review.get("judge_verdict"),
        "market_verdict": internal_review.get("market_verdict"),
        "review_flags": internal_review.get("review_flags") or [],
        "sections": sections,
    }


def update_product_insights_memory(
    submission: dict[str, Any],
    judge_report_text: str | None,
    growth_report_text: str | None,
) -> dict[str, Any]:
    payload = load_product_insights(settings.product_insights_path)
    cases = payload.get("cases") or {}
    snapshot = build_product_insights_case_snapshot(submission, judge_report_text, growth_report_text)
    cases[submission["submission_id"]] = snapshot
    payload["cases"] = cases
    payload["updated_at"] = utc_now_iso()
    save_product_insights(settings.product_insights_path, payload)
    return payload


def aggregate_product_insight_counts(
    payload: dict[str, Any],
) -> tuple[dict[str, list[tuple[str, int]]], list[tuple[str, int]], list[dict[str, Any]]]:
    cases = payload.get("cases") or {}
    section_counts: dict[str, dict[str, dict[str, Any]]] = {
        key: {} for key, _ in PRODUCT_INSIGHT_SECTION_LABELS
    }
    flag_counts: dict[str, int] = {}
    recent_cases = sorted(
        cases.values(),
        key=lambda item: item.get("captured_at") or "",
        reverse=True,
    )[:5]

    for case in cases.values():
        for flag in case.get("review_flags") or []:
            flag_counts[flag] = flag_counts.get(flag, 0) + 1

        sections = case.get("sections") or {}
        for key, _label in PRODUCT_INSIGHT_SECTION_LABELS:
            seen_in_case: set[str] = set()
            for item in sections.get(key) or []:
                normalized_key = normalize_insight_key(item)
                if not normalized_key or normalized_key in seen_in_case:
                    continue
                seen_in_case.add(normalized_key)
                bucket = section_counts[key]
                if normalized_key not in bucket:
                    bucket[normalized_key] = {"text": item, "count": 0}
                bucket[normalized_key]["count"] += 1

    top_sections: dict[str, list[tuple[str, int]]] = {}
    for key, _label in PRODUCT_INSIGHT_SECTION_LABELS:
        buckets = section_counts[key].values()
        top_sections[key] = [
            (item["text"], item["count"])
            for item in sorted(buckets, key=lambda row: (-row["count"], row["text"]))[:5]
        ]

    top_flags = sorted(flag_counts.items(), key=lambda row: (-row[1], row[0]))
    return top_sections, top_flags, recent_cases


def format_product_insights_summary(payload: dict[str, Any]) -> str:
    cases = payload.get("cases") or {}
    if not cases:
        return "Накопленные product insights пока пусты."

    top_sections, top_flags, recent_cases = aggregate_product_insight_counts(payload)
    lines = [
        "Product Insights:",
        f"- Кейсов в памяти: {len(cases)}",
        f"- Обновлено: {payload.get('updated_at') or 'n/a'}",
    ]

    if top_flags:
        flag_text = ", ".join(f"{name} x{count}" for name, count in top_flags[:5])
        lines.append(f"- Частые review flags: {flag_text}")

    for key, label in PRODUCT_INSIGHT_SECTION_LABELS:
        items = top_sections.get(key) or []
        if not items:
            continue
        lines.append("")
        lines.append(f"{label}:")
        for text, count in items[:3]:
            lines.append(f"- x{count}: {text}")

    if recent_cases:
        lines.append("")
        lines.append("Последние кейсы в памяти:")
        for case in recent_cases:
            flags = ", ".join(case.get("review_flags") or []) or "без флагов"
            lines.append(
                f"- {case.get('submission_id')}: {case.get('market_verdict') or 'n/a'}; {flags}"
            )

    return "\n".join(lines)


def utc_timestamp_compact() -> str:
    return datetime.now(UTC_TZ).strftime("%Y%m%d%H%M%S%f")


def build_governance_experiment_id() -> str:
    return f"EXP-{utc_timestamp_compact()}-{uuid4().hex[:6]}"


def build_governance_decision_id() -> str:
    return f"DEC-{utc_timestamp_compact()}-{uuid4().hex[:6]}"


def normalize_governance_title(text: str) -> str:
    return normalize_insight_key(text)


def tokenize_governance_title(text: str) -> set[str]:
    normalized = normalize_governance_title(text)
    if not normalized:
        return set()
    return {token for token in normalized.split() if len(token) >= 4}


def governance_title_similarity(left: str, right: str) -> float:
    left_key = normalize_governance_title(left)
    right_key = normalize_governance_title(right)
    if not left_key or not right_key:
        return 0.0
    if left_key == right_key:
        return 1.0

    left_tokens = tokenize_governance_title(left)
    right_tokens = tokenize_governance_title(right)
    if not left_tokens or not right_tokens:
        return 0.0

    overlap = left_tokens & right_tokens
    union = left_tokens | right_tokens
    if not union:
        return 0.0
    return len(overlap) / len(union)


def is_blocked_by_rejected_experiment(candidate_text: str, experiments: list[dict[str, Any]]) -> dict[str, Any] | None:
    for experiment in experiments:
        if str(experiment.get("status") or "") != "rejected":
            continue
        similarity = governance_title_similarity(candidate_text, str(experiment.get("title") or ""))
        if similarity >= 0.6:
            return experiment
    return None


def sync_governance_experiments_from_insights(payload: dict[str, Any]) -> dict[str, Any]:
    governance = load_product_governance(settings.product_governance_path)
    experiments = governance.get("experiments") or []
    existing_by_key = {
        normalize_governance_title(str(item.get("title") or "")): item for item in experiments
    }

    top_sections, _top_flags, _recent_cases = aggregate_product_insight_counts(payload)
    candidate_sections = (
        ("next_experiments", "next_experiments"),
        ("conversion_ideas", "conversion_ideas"),
        ("retention_ideas", "retention_ideas"),
        ("positioning_upgrades", "positioning_upgrades"),
    )

    changed = False
    for section_key, source_section in candidate_sections:
        for candidate_text, count in (top_sections.get(section_key) or [])[:5]:
            normalized_key = normalize_governance_title(candidate_text)
            if not normalized_key:
                continue

            rejected_match = is_blocked_by_rejected_experiment(candidate_text, experiments)
            if rejected_match:
                blocked_candidates = governance.get("blocked_candidates") or []
                blocked_candidates.insert(
                    0,
                    {
                        "title": candidate_text[:180],
                        "source_section": source_section,
                        "blocked_by": str(rejected_match.get("id") or ""),
                        "blocked_at": utc_now_iso(),
                    },
                )
                governance["blocked_candidates"] = blocked_candidates[:50]
                changed = True
                continue

            existing = existing_by_key.get(normalized_key)
            if existing:
                existing["source_count"] = max(int(existing.get("source_count") or 0), count)
                existing["last_seen_at"] = utc_now_iso()
                existing.setdefault("source_section", source_section)
                changed = True
                continue

            experiment = {
                "id": build_governance_experiment_id(),
                "title": candidate_text[:180],
                "hypothesis": candidate_text,
                "source_section": source_section,
                "source_count": count,
                "status": "proposed",
                "created_at": utc_now_iso(),
                "updated_at": utc_now_iso(),
                "last_seen_at": utc_now_iso(),
                "notes": "",
            }
            experiments.append(experiment)
            existing_by_key[normalized_key] = experiment
            changed = True

    if changed:
        governance["experiments"] = sorted(
            experiments,
            key=lambda item: (item.get("status") != "active", item.get("status") != "proposed", item.get("updated_at") or ""),
            reverse=True,
        )
        governance["updated_at"] = utc_now_iso()
        save_product_governance(settings.product_governance_path, governance)
    return governance

def record_product_decision(
    raw_text: str,
    source: str = "manual_admin",
    *,
    title: str | None = None,
    owner: str = "",
    deadline: str = "",
    kpi: str = "",
) -> dict[str, Any]:
    governance = load_product_governance(settings.product_governance_path)
    decisions = governance.get("decisions") or []
    decision = {
        "id": build_governance_decision_id(),
        "title": (title or raw_text).strip()[:180],
        "details": raw_text,
        "status": "accepted",
        "source": source,
        "owner": owner.strip(),
        "deadline": deadline.strip(),
        "kpi": kpi.strip(),
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    decisions.insert(0, decision)
    governance["decisions"] = decisions[:100]
    governance["updated_at"] = utc_now_iso()
    save_product_governance(settings.product_governance_path, governance)
    return decision


def update_decision_execution(
    decision_id: str,
    *,
    owner: str = "",
    deadline: str = "",
    kpi: str = "",
) -> dict[str, Any] | None:
    governance = load_product_governance(settings.product_governance_path)
    decisions = governance.get("decisions") or []
    for decision in decisions:
        if str(decision.get("id") or "") != decision_id:
            continue
        decision["owner"] = owner.strip()
        decision["deadline"] = deadline.strip()
        decision["kpi"] = kpi.strip()
        decision["updated_at"] = utc_now_iso()
        governance["updated_at"] = utc_now_iso()
        save_product_governance(settings.product_governance_path, governance)
        return decision
    return None


def decision_has_execution_plan(decision: dict[str, Any]) -> bool:
    return bool(
        str(decision.get("owner") or "").strip()
        and str(decision.get("deadline") or "").strip()
        and str(decision.get("kpi") or "").strip()
    )


def get_decision_execution_gaps(
    governance: dict[str, Any],
    *,
    limit: int = 5,
) -> list[dict[str, Any]]:
    decisions = governance.get("decisions") or []
    gaps: list[dict[str, Any]] = []

    for decision in decisions:
        missing_fields: list[str] = []
        if not str(decision.get("owner") or "").strip():
            missing_fields.append("owner")
        if not str(decision.get("deadline") or "").strip():
            missing_fields.append("deadline")
        if not str(decision.get("kpi") or "").strip():
            missing_fields.append("KPI")
        if not missing_fields:
            continue

        gaps.append(
            {
                "id": str(decision.get("id") or ""),
                "title": str(decision.get("title") or ""),
                "missing_fields": missing_fields,
                "updated_at": str(decision.get("updated_at") or ""),
            }
        )

    gaps.sort(key=lambda item: item.get("updated_at") or "", reverse=True)
    return gaps[:limit]


def update_experiment_status(experiment_id: str, new_status: str, note: str = "") -> dict[str, Any] | None:
    governance = load_product_governance(settings.product_governance_path)
    experiments = governance.get("experiments") or []
    for experiment in experiments:
        if str(experiment.get("id")) != experiment_id:
            continue
        experiment["status"] = new_status
        experiment["updated_at"] = utc_now_iso()
        if note:
            existing_notes = str(experiment.get("notes") or "").strip()
            note_line = f"[{utc_now_iso()}] {note}"
            experiment["notes"] = f"{existing_notes}\n{note_line}".strip() if existing_notes else note_line
        governance["updated_at"] = utc_now_iso()
        save_product_governance(settings.product_governance_path, governance)
        return experiment
    return None


def format_governance_summary(governance: dict[str, Any]) -> str:
    decisions = governance.get("decisions") or []
    experiments = governance.get("experiments") or []
    planned_decisions = len([item for item in decisions if decision_has_execution_plan(item)])
    execution_gaps = get_decision_execution_gaps(governance, limit=100)
    status_counts = {status: 0 for status in GOVERNANCE_EXPERIMENT_STATUSES}
    for item in experiments:
        status = str(item.get("status") or "proposed")
        if status not in status_counts:
            status_counts[status] = 0
        status_counts[status] += 1

    lines = [
        "Governance Summary:",
        f"- Decisions: {len(decisions)}",
        f"- Planned decisions: {planned_decisions}",
        f"- Unplanned decisions: {max(len(decisions) - planned_decisions, 0)}",
        f"- Execution gaps: {len(execution_gaps)}",
        f"- Experiments: {len(experiments)}",
        f"- Proposed: {status_counts.get('proposed', 0)}",
        f"- Active: {status_counts.get('active', 0)}",
        f"- Validated: {status_counts.get('validated', 0)}",
        f"- Rejected: {status_counts.get('rejected', 0)}",
        f"- Updated: {governance.get('updated_at') or 'n/a'}",
    ]
    if decisions:
        lines.append(f"- Latest decision: {decisions[0].get('title')}")
    return "\n".join(lines)


def extract_experiment_outcome_memory(
    governance: dict[str, Any],
    *,
    limit_per_status: int = 5,
) -> dict[str, list[dict[str, str]]]:
    experiments = governance.get("experiments") or []
    result: dict[str, list[dict[str, str]]] = {"validated": [], "rejected": []}

    for status in ("validated", "rejected"):
        filtered = [item for item in experiments if str(item.get("status") or "") == status]
        filtered.sort(key=lambda item: str(item.get("updated_at") or ""), reverse=True)
        for item in filtered[:limit_per_status]:
            notes = str(item.get("notes") or "").strip()
            last_note = notes.splitlines()[-1] if notes else ""
            result[status].append(
                {
                    "id": str(item.get("id") or ""),
                    "title": str(item.get("title") or ""),
                    "source_section": str(item.get("source_section") or ""),
                    "updated_at": str(item.get("updated_at") or ""),
                    "note": last_note[:240],
                }
            )

    return result


def build_growth_governance_context(governance: dict[str, Any]) -> dict[str, Any]:
    outcome_memory = extract_experiment_outcome_memory(governance, limit_per_status=5)
    return {
        "validated_learnings": outcome_memory.get("validated", []),
        "rejected_learnings": outcome_memory.get("rejected", []),
        "latest_decisions": [
            {
                "id": str(item.get("id") or ""),
                "title": str(item.get("title") or ""),
                "created_at": str(item.get("created_at") or ""),
            }
            for item in (governance.get("decisions") or [])[:5]
        ],
    }


def format_experiment_outcome_memory(governance: dict[str, Any]) -> str:
    outcome_memory = extract_experiment_outcome_memory(governance, limit_per_status=5)
    validated = outcome_memory.get("validated") or []
    rejected = outcome_memory.get("rejected") or []

    if not validated and not rejected:
        return "Experiment learnings: пока нет validated/rejected экспериментов."

    lines = ["Experiment learnings:", "Validated:"]
    if validated:
        for item in validated[:3]:
            suffix = f" | {item['note']}" if item.get("note") else ""
            lines.append(f"- {item['id']}: {item['title']}{suffix}")
    else:
        lines.append("- Пока нет validated экспериментов.")

    lines.append("Rejected:")
    if rejected:
        for item in rejected[:3]:
            suffix = f" | {item['note']}" if item.get("note") else ""
            lines.append(f"- {item['id']}: {item['title']}{suffix}")
    else:
        lines.append("- Пока нет rejected экспериментов.")

    return "\n".join(lines)


def format_experiments_dashboard(governance: dict[str, Any], limit: int = 10) -> str:
    experiments = governance.get("experiments") or []
    if not experiments:
        return "Experiment tracker пока пуст."

    def sort_key(item: dict[str, Any]) -> tuple[int, int, str]:
        status = str(item.get("status") or "proposed")
        status_rank = {"active": 0, "proposed": 1, "validated": 2, "rejected": 3}.get(status, 4)
        return (status_rank, -int(item.get("source_count") or 0), str(item.get("updated_at") or ""))

    ordered = sorted(experiments, key=sort_key)
    lines = ["Experiment Tracker:"]
    for experiment in ordered[:limit]:
        lines.append("")
        lines.append(f"- {experiment.get('id')} [{experiment.get('status')}]")
        lines.append(f"  {experiment.get('title')}")
        lines.append(f"  Source: {experiment.get('source_section') or 'n/a'} | Signal count: {experiment.get('source_count') or 0}")
        if experiment.get("notes"):
            note_preview = str(experiment.get("notes")).splitlines()[-1]
            lines.append(f"  Note: {note_preview[:180]}")
    return "\n".join(lines)


def format_decisions_dashboard(governance: dict[str, Any], limit: int = 10) -> str:
    decisions = governance.get("decisions") or []
    if not decisions:
        return "Decision log пока пуст."

    lines = ["Decision Log:"]
    for decision in decisions[:limit]:
        lines.append("")
        lines.append(f"- {decision.get('id')} [{decision.get('status')}]")
        lines.append(f"  {decision.get('title')}")
        lines.append(f"  Source: {decision.get('source') or 'n/a'} | At: {decision.get('created_at') or 'n/a'}")
        owner = str(decision.get("owner") or "").strip()
        deadline = str(decision.get("deadline") or "").strip()
        kpi = str(decision.get("kpi") or "").strip()
        if owner or deadline or kpi:
            lines.append(f"  Execution: owner={owner or 'n/a'} | deadline={deadline or 'n/a'} | KPI={kpi or 'n/a'}")
        else:
            lines.append("  Execution: не назначено. Используй /decisionplan <DEC-id> <owner> | <deadline> | <KPI>")
    return "\n".join(lines)


def format_execution_gaps(governance: dict[str, Any], limit: int = 5) -> str:
    gaps = get_decision_execution_gaps(governance, limit=limit)
    if not gaps:
        return "Execution Gaps: все принятые решения уже имеют owner, deadline и KPI."

    lines = ["Execution Gaps:"]
    for item in gaps:
        missing = ", ".join(item.get("missing_fields") or [])
        lines.append("")
        lines.append(f"- {item.get('id')}: {item.get('title')}")
        lines.append(f"  Missing: {missing or 'n/a'}")
        lines.append(f"  Fix: /decisionplan {item.get('id')} <owner> | <deadline> | <KPI>")
    return "\n".join(lines)

def parse_utc_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None


def sort_cases_by_freshness(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def sort_key(case: dict[str, Any]) -> tuple[str, str]:
        internal_review = case.get("internal_review") or {}
        captured_at = case.get("product_insights_updated_at") or case.get("generation_finished_at") or ""
        priority = "1" if internal_review.get("review_flags") else "0"
        return (priority, captured_at)

    return sorted(cases, key=sort_key, reverse=True)


def format_review_dashboard(cases: list[dict[str, Any]], limit: int = 8) -> str:
    if not cases:
        return "Очередь review пока пустая."

    lines = ["Review Dashboard:"]
    for case in sort_cases_by_freshness(cases)[:limit]:
        profile = case.get("profile", {})
        internal_review = case.get("internal_review") or {}
        flags = internal_review.get("review_flags") or []
        status = case.get("intake_status") or "unknown"
        person = profile.get("full_name") or profile.get("telegram_full_name") or "Без имени"
        lines.append("")
        lines.append(f"- {case.get('submission_id')}")
        lines.append(f"  Клиент: {person}")
        lines.append(f"  Статус: {status}")
        lines.append(
            "  Флаги: " + (", ".join(flags) if flags else "без критических внутренних флагов")
        )
        lines.append(
            f"  Judge: {internal_review.get('judge_verdict') or 'n/a'} | Market: {internal_review.get('market_verdict') or 'n/a'}"
        )

    return "\n".join(lines)


def format_windowed_product_summary(payload: dict[str, Any], days: int = 7) -> str:
    cases = payload.get("cases") or {}
    if not cases:
        return f"Weekly Summary ({days}d): память продукта пока пуста."

    cutoff = datetime.now(UTC_TZ).replace(tzinfo=None) - timedelta(days=days)
    filtered_cases: dict[str, Any] = {}
    for case_id, snapshot in cases.items():
        captured_at = parse_utc_iso(snapshot.get("captured_at"))
        if captured_at and captured_at >= cutoff:
            filtered_cases[case_id] = snapshot

    if not filtered_cases:
        return f"Weekly Summary ({days}d): за это окно пока нет накопленных кейсов."

    filtered_payload = {
        "cases": filtered_cases,
        "updated_at": payload.get("updated_at"),
    }
    top_sections, top_flags, recent_cases = aggregate_product_insight_counts(filtered_payload)

    lines = [
        f"Weekly Summary ({days}d):",
        f"- Кейсов в окне: {len(filtered_cases)}",
        f"- Обновлено: {payload.get('updated_at') or 'n/a'}",
    ]

    if top_flags:
        lines.append("- Частые review flags:")
        for name, count in top_flags[:4]:
            lines.append(f"  - {name}: {count}")

    priority_sections = [
        ("demand_risks", "Главные риски спроса"),
        ("value_gaps", "Главные провалы ценности"),
        ("conversion_ideas", "Лучшие идеи конверсии"),
        ("retention_ideas", "Лучшие идеи удержания"),
        ("next_experiments", "Что тестировать дальше"),
    ]
    for key, label in priority_sections:
        items = top_sections.get(key) or []
        if not items:
            continue
        lines.append(f"- {label}:")
        for text, count in items[:3]:
            lines.append(f"  - x{count}: {text}")

    if recent_cases:
        lines.append("- Последние кейсы в окне:")
        for case in recent_cases[:3]:
            flags = ", ".join(case.get("review_flags") or []) or "без флагов"
            lines.append(
                f"  - {case.get('submission_id')}: {case.get('market_verdict') or 'n/a'}; {flags}"
            )

    return "\n".join(lines)


def filter_product_insights_payload_by_days(payload: dict[str, Any], days: int) -> dict[str, Any]:
    cases = payload.get("cases") or {}
    cutoff = datetime.now(UTC_TZ).replace(tzinfo=None) - timedelta(days=days)
    filtered_cases: dict[str, Any] = {}
    for case_id, snapshot in cases.items():
        captured_at = parse_utc_iso(snapshot.get("captured_at"))
        if captured_at and captured_at >= cutoff:
            filtered_cases[case_id] = snapshot

    return {
        "cases": filtered_cases,
        "updated_at": payload.get("updated_at"),
        "digest_state": payload.get("digest_state") or {},
    }


def select_focus_experiments(governance: dict[str, Any], limit: int = 3) -> list[dict[str, Any]]:
    experiments = governance.get("experiments") or []

    def sort_key(item: dict[str, Any]) -> tuple[int, int, str]:
        status = str(item.get("status") or "proposed")
        status_rank = {"active": 0, "proposed": 1, "validated": 2, "rejected": 3}.get(status, 4)
        return (status_rank, -int(item.get("source_count") or 0), str(item.get("updated_at") or ""))

    return sorted(experiments, key=sort_key)[:limit]


def get_validated_source_sections(governance: dict[str, Any]) -> set[str]:
    experiments = governance.get("experiments") or []
    sections: set[str] = set()
    for experiment in experiments:
        if str(experiment.get("status") or "") != "validated":
            continue
        source_section = str(experiment.get("source_section") or "").strip()
        if source_section:
            sections.add(source_section)
    return sections

def format_action_priority_brief(payload: dict[str, Any], governance: dict[str, Any], days: int = 7) -> str:
    filtered_payload = filter_product_insights_payload_by_days(payload, days=days)
    filtered_cases = filtered_payload.get("cases") or {}
    if not filtered_cases and not (governance.get("experiments") or []) and not (governance.get("decisions") or []):
        return f"Action Brief ({days}d): пока недостаточно данных для приоритетов."

    top_sections, _top_flags, _recent_cases = aggregate_product_insight_counts(filtered_payload)
    lines = [f"Action Brief ({days}d):"]
    validated_sections = get_validated_source_sections(governance)

    problem_sections = [
        ("demand_risks", "Главная проблема спроса", {"conversion_ideas", "next_experiments"}),
        ("value_gaps", "Главный провал ценности", {"positioning_upgrades", "retention_ideas", "next_experiments"}),
        ("market_value_risks", "Главный риск премиальной ценности", {"positioning_upgrades", "next_experiments"}),
    ]
    lines.append("- Что болит сильнее всего:")
    problem_added = False
    for section_key, label, solved_by_sections in problem_sections:
        if validated_sections & solved_by_sections:
            continue
        items = top_sections.get(section_key) or []
        if not items:
            continue
        insight_text, count = items[0]
        lines.append(f"  - {label}: x{count} - {insight_text}")
        problem_added = True
    if not problem_added:
        lines.append("  - По главным зонам уже есть validated-решения или пока недостаточно повторения сигналов.")

    decisions = governance.get("decisions") or []
    lines.append("- Последние управленческие решения:")
    if decisions:
        for decision in decisions[:3]:
            lines.append(f"  - {decision.get('id')}: {decision.get('title')}")
    else:
        lines.append("  - Пока нет зафиксированных решений.")

    execution_gaps = get_decision_execution_gaps(governance, limit=3)
    lines.append("- Где исполнение провисает:")
    if execution_gaps:
        for gap in execution_gaps:
            missing = ", ".join(gap.get("missing_fields") or [])
            lines.append(f"  - {gap.get('id')}: не хватает {missing}")
    else:
        lines.append("  - Все принятые решения уже имеют owner, deadline и KPI.")

    focus_experiments = select_focus_experiments(governance, limit=3)
    lines.append("- Что двигать прямо сейчас:")
    if focus_experiments:
        for experiment in focus_experiments:
            lines.append(f"  - {experiment.get('id')} [{experiment.get('status')}]: {experiment.get('title')}")
    else:
        lines.append("  - Пока нет активных или предложенных экспериментов.")

    return "\n".join(lines)


def has_similar_decision_title(candidate_title: str, decisions: list[dict[str, Any]], *, threshold: float = 0.55) -> bool:
    for decision in decisions:
        existing_title = str(decision.get("title") or "")
        if governance_title_similarity(candidate_title, existing_title) >= threshold:
            return True
    return False


def build_suggested_decisions(
    payload: dict[str, Any],
    governance: dict[str, Any],
    *,
    days: int = 7,
    limit: int = 3,
) -> list[dict[str, str]]:
    filtered_payload = filter_product_insights_payload_by_days(payload, days=days)
    top_sections, _top_flags, _recent_cases = aggregate_product_insight_counts(filtered_payload)
    decisions = governance.get("decisions") or []
    validated_sections = get_validated_source_sections(governance)

    suggestions: list[dict[str, str]] = []
    suggested_titles: list[str] = []
    problem_templates = [
        ("demand_risks", {"conversion_ideas", "next_experiments"}, "Снять ключевой барьер спроса: {text}", "Пересобрать первый оффер, стартовый сценарий и вход в продукт так, чтобы этот барьер закрывался в первые касания."),
        ("value_gaps", {"positioning_upgrades", "retention_ideas", "next_experiments"}, "Усилить ядро ценности продукта: {text}", "Уточнить, какой результат и в какой форме получает клиент, чтобы ценность выглядела конкретно, премиально и персонально."),
        ("market_value_risks", {"positioning_upgrades", "next_experiments"}, "Подтвердить премиальную ценность без медицинских обещаний: {text}", "Убрать расплывчатые обещания, усилить деликатную экспертность и показать, за что клиент платит в премиальном сегменте."),
    ]

    for section_key, solved_by_sections, title_template, next_move in problem_templates:
        if len(suggestions) >= limit:
            break
        if validated_sections & solved_by_sections:
            continue
        items = top_sections.get(section_key) or []
        if not items:
            continue
        insight_text, count = items[0]
        title = title_template.format(text=insight_text[:110]).strip()[:180]
        if has_similar_decision_title(title, decisions):
            continue
        if any(governance_title_similarity(title, existing) >= 0.55 for existing in suggested_titles):
            continue
        suggestions.append({
            "title": title,
            "why": f"Сигнал повторился в {count} кейсах за последние {days} дней.",
            "next_move": next_move,
            "source": section_key,
        })
        suggested_titles.append(title)

    if len(suggestions) < limit:
        for experiment in select_focus_experiments(governance, limit=5):
            if len(suggestions) >= limit:
                break
            status = str(experiment.get("status") or "")
            experiment_title = str(experiment.get("title") or "").strip()
            if not experiment_title:
                continue
            if status == "proposed":
                title = f"Перевести в active эксперимент: {experiment_title[:120]}"
                next_move = "Назначить владельца, дедлайн и критерий успеха, чтобы гипотеза дошла до реальной проверки на неделе."
            elif status == "active":
                title = f"Дожать до результата активный эксперимент: {experiment_title[:120]}"
                next_move = "Зафиксировать результат, влияние на конверсию или удержание и принять следующее решение без подвешенного статуса."
            else:
                continue
            title = title[:180]
            if has_similar_decision_title(title, decisions):
                continue
            if any(governance_title_similarity(title, existing) >= 0.55 for existing in suggested_titles):
                continue
            suggestions.append({
                "title": title,
                "why": f"Эксперимент уже находится в governance-фокусе со статусом {status}.",
                "next_move": next_move,
                "source": str(experiment.get("source_section") or "experiment"),
            })
            suggested_titles.append(title)

    return suggestions[:limit]


def format_suggested_decisions(payload: dict[str, Any], governance: dict[str, Any], *, days: int = 7, limit: int = 3) -> str:
    suggestions = build_suggested_decisions(payload, governance, days=days, limit=limit)
    if not suggestions:
        return f"Suggested Decisions ({days}d): пока нет новых решений поверх уже зафиксированных."

    lines = [f"Suggested Decisions ({days}d):"]
    for index, suggestion in enumerate(suggestions, start=1):
        lines.append(f"{index}. {suggestion['title']}")
        lines.append(f"   Почему сейчас: {suggestion['why']}")
        lines.append(f"   Следующий ход: {suggestion['next_move']}")
    lines.append("")
    lines.append("Применить решение: /applydecision <номер>")
    return "\n".join(lines)


def build_suggested_decision_details(suggestion: dict[str, str], *, days: int = 7) -> str:
    lines = [
        suggestion.get("title") or "Suggested decision",
        "",
        f"Почему сейчас: {suggestion.get('why') or 'n/a'}",
        f"Следующий ход: {suggestion.get('next_move') or 'n/a'}",
        f"Источник сигнала: {suggestion.get('source') or 'n/a'}",
        f"Окно анализа: {days}d",
    ]
    return "\n".join(lines)


def apply_suggested_decision(payload: dict[str, Any], governance: dict[str, Any], suggestion_number: int, *, days: int = 7, limit: int = 3) -> tuple[dict[str, Any] | None, str | None]:
    suggestions = build_suggested_decisions(payload, governance, days=days, limit=limit)
    if not suggestions:
        return None, "Сейчас нет доступных suggested decisions для применения."
    if suggestion_number < 1 or suggestion_number > len(suggestions):
        return None, f"Доступны только решения с 1 по {len(suggestions)}."

    suggestion = suggestions[suggestion_number - 1]
    details = build_suggested_decision_details(suggestion, days=days)
    decision = record_product_decision(
        details,
        source="auto_suggestion",
        title=str(suggestion.get("title") or "").strip()[:180],
    )
    return decision, None


def parse_decision_plan_command(raw_text: str) -> tuple[str | None, str | None, str | None, str | None]:
    parts = raw_text.split(maxsplit=2)
    if len(parts) < 3:
        return None, None, None, None
    decision_id = parts[1].strip()
    plan_payload = parts[2].strip()
    if not decision_id or not plan_payload:
        return None, None, None, None
    chunks = [chunk.strip() for chunk in plan_payload.split("|", 2)]
    if len(chunks) != 3 or not all(chunks):
        return decision_id, None, None, None
    return decision_id, chunks[0], chunks[1], chunks[2]


def build_admin_digest_text(payload: dict[str, Any]) -> str:
    weekly_text = format_windowed_product_summary(payload, days=7)
    monthly_text = format_windowed_product_summary(payload, days=30)
    governance = load_product_governance(settings.product_governance_path)
    action_brief = format_action_priority_brief(payload, governance, days=7)
    suggested_decisions_text = format_suggested_decisions(payload, governance, days=7)
    execution_gaps_text = format_execution_gaps(governance, limit=5)
    governance_text = format_governance_summary(governance)
    learnings_text = format_experiment_outcome_memory(governance)
    header = f"Автодайджест продукта ({datetime.now(MOSCOW_TZ).strftime('%Y-%m-%d %H:%M MSK')}):"
    return f"{header}\n\n{action_brief}\n\n{suggested_decisions_text}\n\n{execution_gaps_text}\n\n{weekly_text}\n\n{monthly_text}\n\n{governance_text}\n\n{learnings_text}"


def is_weekly_digest_due(payload: dict[str, Any], now_msk: datetime | None = None) -> bool:
    now_msk = now_msk or datetime.now(MOSCOW_TZ)
    if now_msk.weekday() != 0:
        return False
    if now_msk.hour < 10:
        return False
    digest_state = payload.get("digest_state") or {}
    current_week_key = now_msk.strftime("%G-W%V")
    return digest_state.get("weekly_last_sent_week") != current_week_key


def mark_weekly_digest_sent(payload: dict[str, Any], now_msk: datetime | None = None) -> dict[str, Any]:
    now_msk = now_msk or datetime.now(MOSCOW_TZ)
    digest_state = payload.get("digest_state") or {}
    digest_state["weekly_last_sent_week"] = now_msk.strftime("%G-W%V")
    digest_state["last_sent_at"] = now_msk.strftime("%Y-%m-%dT%H:%M:%SZ")
    payload["digest_state"] = digest_state
    payload["updated_at"] = utc_now_iso()
    return payload

