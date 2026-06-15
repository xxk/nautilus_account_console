from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

from nautilus_account_console.ctp19053_consistency import (  # noqa: E402
    DEFAULT_BLOCKER_PATH,
    DEFAULT_SOURCE_PACKAGE,
    evaluate_ctp19053_source_package,
    write_blocker_if_needed,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-package", type=Path, default=DEFAULT_SOURCE_PACKAGE)
    parser.add_argument("--blocker-path", type=Path, default=DEFAULT_BLOCKER_PATH)
    parser.add_argument("--write-blocker", action="store_true")
    args = parser.parse_args()

    if args.write_blocker:
        result = write_blocker_if_needed(args.source_package, args.blocker_path)
    else:
        result = evaluate_ctp19053_source_package(args.source_package)

    payload = result.to_dict()
    print(json.dumps(payload, sort_keys=True))
    if result.verdict == "passed":
        print("CTP19053_CONSISTENCY_OK: verdict=passed")
    elif result.verdict == "blocked":
        print(f"CTP19053_CONSISTENCY_BLOCKED: blocker={result.blocker_id}")
    else:
        raise AssertionError(f"unexpected verdict: {result.verdict}")


if __name__ == "__main__":
    main()
