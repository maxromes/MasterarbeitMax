#!/usr/bin/env python3
"""
Rebuilds the core analysis outputs in a deterministic order.

Usage:
    python scripts/rebuild_core_results.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SCRIPTS = [
    "scripts/species_richness_cut47min_analysis.py",
    "scripts/standortvergleich_cut47min_analysis.py",
    "scripts/update_visibility_analysis.py",
    "scripts/visibility_adjusted_models.py",
    "scripts/visibility_additional_tests.py",
    "scripts/visibility_site_stratified_tests.py",
]


def main() -> int:
    python_exe = sys.executable
    print(f"Using Python: {python_exe}")

    for rel_path in SCRIPTS:
        script_path = ROOT / rel_path
        print(f"\n[RUN] {rel_path}")
        result = subprocess.run([python_exe, str(script_path)], cwd=str(ROOT))
        if result.returncode != 0:
            print(f"[FAIL] {rel_path} (exit={result.returncode})")
            return result.returncode
        print(f"[OK] {rel_path}")

    print("\nCore rebuild finished successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
