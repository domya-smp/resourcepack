#!/usr/bin/env python3
"""Validate and package the resource pack using only the Python standard library."""

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
ARCHIVE_NAME = "domsmp.zip"


def main() -> None:
    assets = ROOT / "assets"
    if not assets.is_dir():
        raise SystemExit("Missing assets directory")

    asset_files = sorted(path for path in assets.rglob("*") if path.is_file())
    if not asset_files:
        raise SystemExit("The assets directory is empty")

    files = [ROOT / "pack.mcmeta", ROOT / "pack.png", *asset_files]
    for path in files:
        if not path.is_file():
            raise SystemExit(f"Missing required file: {path.relative_to(ROOT)}")
        if path.suffix in {".json", ".mcmeta"}:
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (ValueError, UnicodeError) as error:
                raise SystemExit(f"Invalid JSON in {path.relative_to(ROOT)}: {error}") from error

    DIST.mkdir(exist_ok=True)
    archive_path = DIST / ARCHIVE_NAME
    with ZipFile(archive_path, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            # Stable timestamps, order and permissions keep builds reproducible.
            info = ZipInfo(path.relative_to(ROOT).as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)

    print(f"Built {archive_path.relative_to(ROOT)} ({len(files)} files, {archive_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
