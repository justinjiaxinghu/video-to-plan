#!/usr/bin/env python3
"""
Promote an engineering plan into a git-ready directory.

Takes the generated engineering_plan.md and cached artifacts (.cache/) and
packages them into a clean, named directory with a README and metadata.

Usage:
  python promote_plan.py my-saas-product
  python promote_plan.py my-saas-product --plan path/to/engineering_plan.md
  python promote_plan.py my-saas-product --plan plan.md --cache path/to/.cache
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


def promote(name: str, plan_path: Path, cache_dir: Path, output_root: Path) -> Path:
    dest = output_root / name
    if dest.exists():
        print(f"Error: directory already exists: {dest}", file=sys.stderr)
        print("  Pick a different name or remove it first.", file=sys.stderr)
        sys.exit(1)

    # Create structure
    dest.mkdir(parents=True)
    (dest / "artifacts").mkdir()

    # Copy the plan
    shutil.copy2(plan_path, dest / "PRD.md")
    print(f"  Copied plan → {dest / 'PRD.md'}")

    # Copy cached artifacts if available
    copied_artifacts = []
    for filename in ["visual_analysis.json", "synthesis.json"]:
        src = cache_dir / filename
        if src.exists():
            shutil.copy2(src, dest / "artifacts" / filename)
            copied_artifacts.append(filename)
            print(f"  Copied artifact → artifacts/{filename}")

    # Write metadata
    metadata = {
        "name": name,
        "promoted_at": datetime.now().isoformat(),
        "source_plan": str(plan_path),
        "source_cache": str(cache_dir),
        "artifacts": copied_artifacts,
    }
    (dest / "artifacts" / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )

    # Generate README
    readme_lines = [
        f"# {name}",
        "",
        f"Engineering plan promoted on {datetime.now().strftime('%Y-%m-%d')}.",
        "",
        "## Contents",
        "",
        "- **PRD.md** — Product Requirements Document",
    ]
    if "visual_analysis.json" in copied_artifacts:
        readme_lines.append("- **artifacts/visual_analysis.json** — Timestamped visual observations from source video")
    if "synthesis.json" in copied_artifacts:
        readme_lines.append("- **artifacts/synthesis.json** — Synthesized pain points, workflows, and requirements")
    readme_lines.append("- **artifacts/metadata.json** — Promotion metadata")
    readme_lines.append("")

    (dest / "README.md").write_text("\n".join(readme_lines))
    print(f"  Generated → README.md")

    return dest


def main():
    parser = argparse.ArgumentParser(
        description="Promote an engineering plan into a git-ready directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python promote_plan.py my-saas-product
  python promote_plan.py my-saas-product --plan path/to/engineering_plan.md
  python promote_plan.py my-saas-product --output-root ~/projects/plans
        """,
    )
    parser.add_argument("name", help="Directory name for the promoted plan (e.g. my-saas-product)")
    parser.add_argument("--plan", default="engineering_plan.md", help="Path to engineering plan (default: engineering_plan.md)")
    parser.add_argument("--cache", default=".cache", help="Path to .cache directory with artifacts (default: .cache)")
    parser.add_argument("--output-root", default=".", help="Parent directory for the promoted plan (default: current dir)")

    args = parser.parse_args()

    plan_path = Path(args.plan).resolve()
    cache_dir = Path(args.cache).resolve()
    output_root = Path(args.output_root).resolve()

    if not plan_path.exists():
        print(f"Error: plan not found: {plan_path}", file=sys.stderr)
        sys.exit(1)

    if not cache_dir.exists():
        print(f"Warning: cache directory not found: {cache_dir}", file=sys.stderr)
        print("  Promoting plan without artifacts.", file=sys.stderr)
        cache_dir = Path("/nonexistent")  # will just skip artifact copies

    print(f"Promoting: {args.name}")
    dest = promote(args.name, plan_path, cache_dir, output_root)

    print(f"\nDone. Directory ready at: {dest}")
    print(f"\n  cd {dest} && git init && git add -A && git commit -m 'Initial PRD'")


if __name__ == "__main__":
    main()
