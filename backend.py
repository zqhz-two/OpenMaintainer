"""Minimal PEP 517 backend for offline editable installs."""
from __future__ import annotations

import base64
import hashlib
import os
from pathlib import Path
import zipfile

NAME = "openmaintainer"
VERSION = "0.1.0"
DIST = f"{NAME}-{VERSION}.dist-info"


def _wheel_name() -> str:
    return f"{NAME}-{VERSION}-py3-none-any.whl"


def _metadata() -> str:
    return f"Metadata-Version: 2.1\nName: {NAME}\nVersion: {VERSION}\nSummary: GitHub 开源仓库维护 Agent Demo\n"


def _wheel_file() -> str:
    return "Wheel-Version: 1.0\nGenerator: custom-backend\nRoot-Is-Purelib: true\nTag: py3-none-any\n"


def _entry_points() -> str:
    return "[console_scripts]\nopenmaintainer = openmaintainer.runner:main\n"


def _record_line(path: str, data: bytes) -> str:
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")
    return f"{path},sha256={digest},{len(data)}\n"


def _build_wheel(wheel_directory: str, editable: bool) -> str:
    wheel_directory_path = Path(wheel_directory)
    wheel_directory_path.mkdir(parents=True, exist_ok=True)
    wheel_name = _wheel_name()
    wheel_path = wheel_directory_path / wheel_name

    src_root = Path("src").resolve()
    files: dict[str, bytes] = {
        f"{DIST}/METADATA": _metadata().encode(),
        f"{DIST}/WHEEL": _wheel_file().encode(),
        f"{DIST}/entry_points.txt": _entry_points().encode(),
    }

    if editable:
        pth_name = f"{NAME}.pth"
        files[pth_name] = (str(src_root) + os.linesep).encode()
    else:
        for path in (src_root / NAME).rglob("*.py"):
            rel = path.relative_to(src_root).as_posix()
            files[rel] = path.read_bytes()

    record = "".join(_record_line(path, data) for path, data in files.items())
    record += f"{DIST}/RECORD,,\n"
    files[f"{DIST}/RECORD"] = record.encode()

    with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path, data in files.items():
            zf.writestr(path, data)

    return wheel_name


def build_wheel(wheel_directory: str, config_settings=None, metadata_directory=None) -> str:
    return _build_wheel(wheel_directory, editable=False)


def build_editable(wheel_directory: str, config_settings=None, metadata_directory=None) -> str:
    return _build_wheel(wheel_directory, editable=True)


def get_requires_for_build_wheel(config_settings=None):
    return []


def get_requires_for_build_editable(config_settings=None):
    return []


def prepare_metadata_for_build_wheel(metadata_directory: str, config_settings=None):
    md = Path(metadata_directory) / DIST
    md.mkdir(parents=True, exist_ok=True)
    (md / "METADATA").write_text(_metadata(), encoding="utf-8")
    (md / "WHEEL").write_text(_wheel_file(), encoding="utf-8")
    return DIST


def prepare_metadata_for_build_editable(metadata_directory: str, config_settings=None):
    return prepare_metadata_for_build_wheel(metadata_directory, config_settings)
