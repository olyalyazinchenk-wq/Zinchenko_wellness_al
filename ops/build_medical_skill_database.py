from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from medical_skill_database import export_medical_skill_database  # noqa: E402


def main() -> None:
    output_path = BOT_DIR / "data" / "medical_skill_database.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = export_medical_skill_database()
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "ok",
                "path": str(output_path),
                "version": payload["version"],
                "marker_count": len(payload["markers"]),
                "symptom_route_count": len(payload["symptom_routes"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
