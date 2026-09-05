"""
Run the complete Kin Bakeshop sales-analysis pipeline.

Usage:
    python run_analysis.py

Optional:
    python run_analysis.py --input-dir data --output-dir outputs --charts-dir charts
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


STEPS = [
    "src/01_load_clean.py",
    "src/02_yearly_summary.py",
    "src/03_classify_menu.py",
    "src/04_yoy_analysis.py",
    "src/05_charts.py",
]


def run_step(script: str, input_dir: Path, output_dir: Path, charts_dir: Path) -> None:
    command = [
        sys.executable,
        script,
        "--output-dir",
        str(output_dir),
    ]

    if script.endswith("01_load_clean.py"):
        command.extend(["--input-dir", str(input_dir)])
    elif script.endswith("05_charts.py"):
        command.extend(["--charts-dir", str(charts_dir)])

    print("\n" + "=" * 70)
    print(f"Running {script}")
    print("=" * 70)

    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=Path("data"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--charts-dir", type=Path, default=Path("charts"))
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.charts_dir.mkdir(parents=True, exist_ok=True)

    for step in STEPS:
        run_step(
            step,
            args.input_dir,
            args.output_dir,
            args.charts_dir,
        )

    print("\nPipeline complete.")
    print(f"Outputs: {args.output_dir}")
    print(f"Charts:  {args.charts_dir}")


if __name__ == "__main__":
    main()
