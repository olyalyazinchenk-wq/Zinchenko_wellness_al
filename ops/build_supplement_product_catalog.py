from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_DIR = PROJECT_ROOT / "WellnessBot"
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

from supplement_product_catalog import export_supplement_catalog  # noqa: E402


def main() -> None:
    output_path = BOT_DIR / "data" / "supplement_product_catalog.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = export_supplement_catalog()
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "ok",
                "path": str(output_path),
                "version": payload["version"],
                "product_count": len(payload["products"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
