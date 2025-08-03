#!/usr/bin/env python3
import argparse
import logging
import shutil
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_EXCLUDED_EXTENSIONS = {'.tmp', '.crdownload', '.part', '.ds_store'}

def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=level)

def parse_excluded_exts(ext_string: str) -> set[str]:
    return {ext.lower() if ext.startswith('.') else f".{ext.lower()}" for ext in ext_string.split(',')} if ext_string else DEFAULT_EXCLUDED_EXTENSIONS

def should_exclude(file: Path, excluded_exts: set[str]) -> bool:
    return file.suffix.lower() in excluded_exts

def organize_by_year_month(file_path: Path) -> Path:
    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    return Path(str(mtime.year), f"{mtime.month:02}")

def organize_by_year_extension(file_path: Path) -> Path:
    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    ext = file_path.suffix.lower().lstrip('.') or 'no_extension'
    return Path(str(mtime.year), ext)

def should_include_by_days(file_path: Path, max_age_days: int) -> bool:
    if max_age_days is None:
        return True
    age_limit = datetime.now() - timedelta(days=max_age_days)
    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    return mtime >= age_limit

def main(downloads_dir: str, mode: str, dry_run: bool, max_age_days: int, verbose: bool, excluded_exts: set[str]):
    setup_logging(verbose)
    base_path = Path(downloads_dir).expanduser()
    organized_dir = base_path / "organized"

    if not base_path.exists():
        logging.error(f"Directory not found: {base_path}")
        return

    logging.info(f"Scanning directory: {base_path}")
    logging.debug(f"Excluded extensions: {excluded_exts}")

    for file_path in base_path.rglob('*'):
    #for file_path in base_path.iterdir():
        if file_path.is_file() and not should_exclude(file_path, excluded_exts) and should_include_by_days(file_path, max_age_days):
            if mode == "year_month":
                target_subdir = organize_by_year_month(file_path)
            elif mode == "year_extension":
                target_subdir = organize_by_year_extension(file_path)
            else:
                logging.error(f"Invalid mode: {mode}")
                return

            destination = organized_dir / target_subdir
            destination.mkdir(parents=True, exist_ok=True)
            dest_path = destination / file_path.name

            if dry_run:
                logging.info(f"[Dry run] Would move: {file_path.name} → {dest_path}")
            else:
                shutil.move(str(file_path), dest_path)
                logging.info(f"Moved: {file_path.name} → {dest_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files in your Downloads folder.")
    parser.add_argument("--dir", default="~/Downloads", help="Directory to organize (default: ~/Downloads)")
    parser.add_argument("--mode", choices=["year_month", "year_extension"], default="year_month",
                        help="Organization mode: by year/month or year/extension")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without moving files")
    parser.add_argument("--days", type=int, default=None, help="Only include files modified in the last N days")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--exclude-exts", type=str, default=None,
                        help="Comma-separated list of file extensions to exclude (e.g. .tmp,.part)")

    args = parser.parse_args()
    excluded_exts = parse_excluded_exts(args.exclude_exts)
    main(args.dir, args.mode, args.dry_run, args.days, args.verbose, excluded_exts)