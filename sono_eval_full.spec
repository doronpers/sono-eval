# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
from pathlib import Path

block_cipher = None

# Base directory
base_dir = Path.cwd()

# Initialize lists
datas = [('alembic.ini', '.')]
binaries = []
hiddenimports = [
    "uvicorn.loops.auto",
    "uvicorn.protocols.http.auto",
    "uvicorn.lifespan.on",
    "pg8000",
    "sqlite3",
    "sqlalchemy.dialects.sqlite",
    "sqlalchemy.dialects.postgresql",
]

# Collect ML dependencies
print("Collecting ML dependencies...")
pkgs = [
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
    "yaml"
]

for package in pkgs:
    try:
        d, b, h = collect_all(package)
        datas.extend(d)
        binaries.extend(b)
        hiddenimports.extend(h)
        print(f"Collected {package}")
    except Exception as e:
        print(f"Warning: Failed to collect {package}: {e}")

a = Analysis(
    [str(base_dir / 'src/sono_eval/cli/standalone.py')],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='sono-eval-full',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
