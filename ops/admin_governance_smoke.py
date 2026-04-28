from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

import governance_service as gs  # noqa: E402
from storage import list_recent_cases  # noqa: E402


def build_fixture_submission(base_dir: Path) -> dict:
    fixture_path = base_dir / "data" / "submissions" / "20260413T205558Z_1084557944.json"
    submission = json.loads(fixture_path.read_text(encoding="utf-8"))
    submission["internal_review"] = {
        "judge_verdict": "needs_rework",
        "market_verdict": "stronger_positioning_needed",
        "review_flags": ["quality_rework", "market_rework"],
    }
    submission["product_insights_updated_at"] = "2026-04-21T00:00:00Z"
    return submission


def build_fixture_reports() -> tuple[str, str]:
    judge_report = json.dumps(
        {
            "market_value_risks": [
                "Премиальная ценность описана слишком расплывчато",
                "Нет четкой разницы между AI-черновиком и персональным разбором специалиста",
            ]
        },
        ensure_ascii=False,
    )
    growth_report = json.dumps(
        {
            "demand_risks": [
                "Клиенту неочевидно, какой конкретный результат он получает на выходе",
                "Слишком широкий оффер без ясного первого сценария входа",
            ],
            "value_gaps": [
                "Не хватает структуры следующего шага после анкеты",
            ],
            "positioning_upgrades": [
                "Подчеркнуть деликатную нутрициологическую навигацию без медицинских обещаний",
            ],
            "conversion_ideas": [
                "Показать пример итогового разбора и формат персонального сопровождения",
            ],
            "retention_ideas": [
                "Добавить follow-up касание после выдачи разбора",
            ],
            "referral_ideas": [
                "Ввести мягкий реферальный сценарий после получения результата",
            ],
            "next_experiments": [
                "Протестировать более конкретный оффер с акцентом на персональный план действий",
            ],
        },
        ensure_ascii=False,
    )
    return judge_report, growth_report


def ensure_smoke_dirs(smoke_dir: Path) -> tuple[Path, Path, Path, Path, Path, Path]:
    submissions_dir = smoke_dir / "submissions"
    uploads_dir = smoke_dir / "uploads"
    drafts_dir = smoke_dir / "drafts"
    for directory in (smoke_dir, submissions_dir, uploads_dir, drafts_dir):
        directory.mkdir(parents=True, exist_ok=True)

    product_insights_path = smoke_dir / "product_insights.json"
    product_governance_path = smoke_dir / "product_governance.json"
    runtime_state_path = smoke_dir / "runtime_state.json"

    for path in (product_insights_path, product_governance_path, runtime_state_path):
        if path.exists():
            path.unlink()

    return (
        submissions_dir,
        uploads_dir,
        drafts_dir,
        product_insights_path,
        product_governance_path,
        runtime_state_path,
    )


def main() -> int:
    smoke_dir = BOT_DIR / "data" / "smoke_admin_governance"
    (
        submissions_dir,
        uploads_dir,
        drafts_dir,
        product_insights_path,
        product_governance_path,
        runtime_state_path,
    ) = ensure_smoke_dirs(smoke_dir)

    original_settings = gs.settings
    gs.settings = replace(
        gs.settings,
        data_dir=smoke_dir,
        submissions_dir=submissions_dir,
        uploads_dir=uploads_dir,
        drafts_dir=drafts_dir,
        runtime_state_path=runtime_state_path,
        product_insights_path=product_insights_path,
        product_governance_path=product_governance_path,
    )

    try:
        submission = build_fixture_submission(BOT_DIR)
        judge_report, growth_report = build_fixture_reports()

        recent_cases = list_recent_cases(BOT_DIR / "data" / "submissions", limit=10)
        review_dashboard = gs.format_review_dashboard(recent_cases, limit=5)
        empty_insights_text = gs.format_product_insights_summary(
            {"cases": {}, "updated_at": None}
        )
        empty_governance_text = gs.format_governance_summary(
            {"decisions": [], "experiments": [], "updated_at": None}
        )

        payload = gs.update_product_insights_memory(submission, judge_report, growth_report)
        gs.sync_governance_experiments_from_insights(payload)

        decision = gs.record_product_decision(
            "Запустить проверку нового оффера и структуры выдачи на 5 ближайших кейсах.",
            source="smoke_test",
            title="Проверить новый оффер и структуру выдачи",
        )
        gs.update_decision_execution(
            decision["id"],
            owner="Olga",
            deadline="2026-04-28",
            kpi="5 кейсов с новым оффером и обратной связью по конверсии",
        )
        updated_governance = json.loads(product_governance_path.read_text(encoding="utf-8"))

        report_sections = [
            "# Smoke Report: Admin / Governance / Digest",
            "",
            "## Scope",
            "- real saved submission used as fixture",
            "- isolated smoke data directory used instead of production governance files",
            "- exercised insights accumulation, governance sync, decision record, execution update, review dashboard, and digest generation",
            "",
            "## Empty State",
            f"- Product insights: {empty_insights_text}",
            f"- Governance summary first line: {empty_governance_text.splitlines()[0] if empty_governance_text else 'n/a'}",
            "",
            "## Review Dashboard Preview",
            "```text",
            review_dashboard,
            "```",
            "",
            "## Generated Files",
            f"- {product_insights_path}",
            f"- {product_governance_path}",
            "",
            "## Product Insights Summary",
            "```text",
            gs.format_product_insights_summary(payload),
            "```",
            "",
            "## Governance Summary",
            "```text",
            gs.format_governance_summary(updated_governance),
            "```",
            "",
            "## Experiments Dashboard",
            "```text",
            gs.format_experiments_dashboard(updated_governance),
            "```",
            "",
            "## Decisions Dashboard",
            "```text",
            gs.format_decisions_dashboard(updated_governance),
            "```",
            "",
            "## Action Brief",
            "```text",
            gs.format_action_priority_brief(payload, updated_governance, days=7),
            "```",
            "",
            "## Suggested Decisions",
            "```text",
            gs.format_suggested_decisions(payload, updated_governance, days=7),
            "```",
            "",
            "## Digest",
            "```text",
            gs.build_admin_digest_text(payload),
            "```",
            "",
            "## Weekly Digest State",
            f"- due_now: {gs.is_weekly_digest_due(payload)}",
            f"- after_mark: {gs.mark_weekly_digest_sent(dict(payload)).get('digest_state')}",
        ]

        report_path = PROJECT_ROOT / "docs" / "SMOKE_ADMIN_GOVERNANCE_20260421.md"
        report_path.write_text("\n".join(report_sections), encoding="utf-8")

        print("SMOKE_OK")
        print(f"report={report_path}")
        print(f"product_insights_exists={product_insights_path.exists()}")
        print(f"product_governance_exists={product_governance_path.exists()}")
        print(f"experiments={len(updated_governance.get('experiments') or [])}")
        print(f"decisions={len(updated_governance.get('decisions') or [])}")
        return 0
    finally:
        gs.settings = original_settings


if __name__ == "__main__":
    raise SystemExit(main())
