from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
WELLNESS_BOT = ROOT / "WellnessBot"
if str(WELLNESS_BOT) not in sys.path:
    sys.path.insert(0, str(WELLNESS_BOT))

from ai_drafting import generate_live_reply  # noqa: E402
from config import load_settings  # noqa: E402


def run_smoke() -> int:
    settings = load_settings()
    prompt = "После завершения досье как будет продолжаться общение? Мне нужно будет куда-то переходить или всё останется здесь?"
    reply = generate_live_reply(settings, [], prompt) or ""
    print("=== smoke-reply ===")
    print(reply[:800] if reply else "EMPTY")
    return 0 if reply else 1


def run_batch(prompts_file: Path) -> int:
    settings = load_settings()
    prompts = json.loads(prompts_file.read_text(encoding="utf-8"))
    if not isinstance(prompts, list) or not prompts:
        print("Prompts file is empty or invalid.")
        return 1

    rows: list[dict[str, str]] = []
    for idx, prompt in enumerate(prompts, start=1):
        text = str(prompt).strip()
        if not text:
            continue
        reply = generate_live_reply(settings, [], text) or ""
        rows.append(
            {
                "id": str(idx),
                "prompt": text,
                "reply": reply.strip(),
                "empty": "yes" if not reply.strip() else "no",
            }
        )

    reports_dir = ROOT / "ops" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    out = reports_dir / f"quality_report_{stamp}.md"

    lines = [
        f"# Quality Report {stamp}",
        "",
        f"Total prompts: {len(rows)}",
        f"Empty replies: {sum(1 for row in rows if row['empty'] == 'yes')}",
        "",
    ]
    for row in rows:
        lines.append(f"## Prompt {row['id']}")
        lines.append("")
        lines.append(f"Prompt: {row['prompt']}")
        lines.append("")
        lines.append("Reply:")
        lines.append(row["reply"] if row["reply"] else "<EMPTY>")
        lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report generated: {out}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Live dialogue quality probe")
    parser.add_argument("--mode", choices=["smoke", "batch"], required=True)
    parser.add_argument("--prompts", type=Path, help="Path to prompts json for batch mode")
    args = parser.parse_args()

    if args.mode == "smoke":
        return run_smoke()

    if not args.prompts:
        print("--prompts is required in batch mode")
        return 1
    return run_batch(args.prompts)


if __name__ == "__main__":
    raise SystemExit(main())
