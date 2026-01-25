#!/usr/bin/env python3
"""
Build script for Sono-Eval Standalone Executable.

This script uses PyInstaller to build a single-file executable of the
application, including all necessary dependencies and data files.
"""

import os
import shutil
import subprocess  # nosec B404
import sys
from pathlib import Path


def build():
    """Run PyInstaller to build the standalone executable."""
    base_dir = Path(__file__).resolve().parent.parent
    os.chdir(base_dir)

    print(f"Build directory: {base_dir}")

    import argparse

    from PyInstaller.utils.hooks import collect_all

    parser = argparse.ArgumentParser(description="Build Sono-Eval Standalone")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Include full ML dependencies (torch, transformers)",
    )
    args_cli = parser.parse_args()

    mode = "full" if args_cli.full else "light"
    print(f"Building in {mode} mode...")

    # Define build arguments
    args = [
        "pyinstaller",
        "--noconfirm",
        "--clean",
        "--name",
        "sono-eval",
        "--onefile",  # Create a single executable
        # Entry point
        str(base_dir / "src/sono_eval/cli/standalone.py"),
        # Hidden imports (FastAPI/Uvicorn/SQLAlchemy/etc often need these)
        "--hidden-import",
        "uvicorn.loops.auto",
        "--hidden-import",
        "uvicorn.protocols.http.auto",
        "--hidden-import",
        "uvicorn.lifespan.on",
        "--hidden-import",
        "pg8000",
        "--hidden-import",
        "sqlite3",
        "--hidden-import",
        "sqlalchemy.dialects.sqlite",
        "--hidden-import",
        "sqlalchemy.dialects.postgresql",
        # Data files
        "--add-data",
        "alembic.ini:.",
        # Add src/sono_eval as package data if needed for non-code resources
        # "--add-data", "src/sono_eval:sono_eval",
        # Paths
        "--workpath",
        "build",
        "--distpath",
        "dist",
    ]

    if args_cli.full:
        print(
            "Collecting ML dependencies (this will increase build size significantly)..."
        )
        # Collect all data, binaries, and hidden imports for ML packages
        for package in [
            "torch",
            "transformers",
            "peft",
            "sentencepiece",
            "accelerate",
            "tqdm",
            "regex",
            "requests",
            "packaging",
            "filelock",
            "numpy",
            "yaml",
        ]:
            try:
                datas, binaries, hiddenimports = collect_all(package)
                for src, dest in datas:
                    args.extend(["--add-data", f"{src}:{dest}"])
                for src, dest in binaries:
                    args.extend(["--add-binary", f"{src}:{dest}"])
                for hidden in hiddenimports:
                    args.extend(["--hidden-import", hidden])
            except Exception as e:
                print(f"Warning: Failed to collect {package}: {e}")

    print(f"Running command: {' '.join(args)}")

    try:
        subprocess.run(args, check=True)  # nosec B603
        print("\n✅ Build successful!")
        print(f"Executable created at: {base_dir}/dist/sono-eval")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with exit code {e.returncode}")
        sys.exit(1)


if __name__ == "__main__":
    # Check if pyinstaller is installed
    if shutil.which("pyinstaller") is None:
        print("❌ Error: PyInstaller not found. Please run 'pip install pyinstaller'")
        sys.exit(1)

    build()
