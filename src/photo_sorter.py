#!/usr/bin/env python3
"""
====================================================
  SOUTHDREAMS PHOTO SORTER v2.0
  by SouthDreams | Dirty Road Creations
  github.com/southdreams
====================================================
  Sorts your messy photo folders into clean structure:
  2024/January/Photos/
  2024/January/Videos/
  2024/January/RAW/
  2024/January/Screenshots/
  2024/January/Other/

  Features:
  - Sorts by Year / Month / File Type
  - Detects duplicates and asks what to do
  - Renames files to their date
  - Generates a full report of everything moved
  - Handles RAW camera files (CR2, NEF, ARW, DNG)
  - Safe preview mode by default
====================================================
"""

import os
import shutil
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Try to import Pillow for reading photo EXIF data
# EXIF data is the hidden info inside a photo (date taken, camera model, etc.)
try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


# ── FILE TYPE DEFINITIONS ────────────────────────────────────────────────────
# These are all the file extensions we recognize and where they go

FILE_TYPES = {
    "Photos":      [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".tiff", ".tif"],
    "Videos":      [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".m4v", ".3gp", ".mts"],
    "RAW":         [".cr2", ".cr3", ".nef", ".arw", ".dng", ".orf", ".rw2", ".pef", ".raf"],
    "Screenshots": [".png"],  # We check filename too — "screenshot" in the name
}

MONTH_NAMES = {
    1: "January",   2: "February",  3: "March",
    4: "April",     5: "May",       6: "June",
    7: "July",      8: "August",    9: "September",
    10: "October",  11: "November", 12: "December"
}


# ── STEP 1: GET FILE DATE ────────────────────────────────────────────────────
# Try to get the REAL date a photo was taken from its EXIF data.
# If that fails, fall back to the file's last modified date.

def get_file_date(filepath):
    """Return a datetime object for when this file was created/taken."""

    # Try EXIF data first (most accurate — this is the date the photo was taken)
    if PILLOW_AVAILABLE and filepath.suffix.lower() in [".jpg", ".jpeg", ".tiff", ".tif"]:
        try:
            img = Image.open(filepath)
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "DateTimeOriginal":
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        except Exception:
            pass  # If EXIF fails just move on

    # Fall back to file modified date
    timestamp = filepath.stat().st_mtime
    return datetime.fromtimestamp(timestamp)


# ── STEP 2: FIGURE OUT FILE TYPE ─────────────────────────────────────────────

def get_file_category(filepath):
    """Return which category folder this file belongs in."""
    ext = filepath.suffix.lower()
    name = filepath.name.lower()

    # Check if it's a screenshot by name
    if "screenshot" in name and ext in FILE_TYPES["Photos"]:
        return "Screenshots"

    # Check RAW first (some RAW formats overlap with other types)
    if ext in FILE_TYPES["RAW"]:
        return "RAW"

    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category

    return "Other"


# ── STEP 3: GET FILE FINGERPRINT ─────────────────────────────────────────────

def get_file_hash(filepath):
    """Get the fingerprint (MD5 hash) of a file to detect duplicates."""
    hasher = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (OSError, PermissionError):
        return None


# ── STEP 4: BUILD NEW FILENAME ───────────────────────────────────────────────

def build_new_filename(filepath, file_date):
    """
    Rename the file to its date.
    Example: IMG_4823.jpg → 2024-03-15_IMG_4823.jpg
    """
    date_prefix = file_date.strftime("%Y-%m-%d")
    original_name = filepath.name

    # Don't add the prefix twice if it's already there
    if original_name.startswith(date_prefix):
        return original_name

    return f"{date_prefix}_{original_name}"


# ── STEP 5: SCAN ALL FILES ───────────────────────────────────────────────────

def scan_folder(source_folder):
    """Scan the folder and return a list of all files with their info."""
    source_path = Path(source_folder)

    if not source_path.exists():
        print(f"\n  [ERROR] Folder not found: {source_folder}")
        return []

    print(f"\n  Scanning: {source_path.resolve()}")
    print("  Please wait...\n")

    all_files = [f for f in source_path.rglob("*") if f.is_file()]
    total = len(all_files)
    print(f"  Found {total} file(s). Analyzing...\n")

    file_list = []
    for i, filepath in enumerate(all_files, 1):
        print(f"  [{i}/{total}] {filepath.name}", end="\r")
        file_date = get_file_date(filepath)
        category  = get_file_category(filepath)
        file_hash = get_file_hash(filepath)
        new_name  = build_new_filename(filepath, file_date)

        file_list.append({
            "path":      filepath,
            "date":      file_date,
            "category":  category,
            "hash":      file_hash,
            "new_name":  new_name,
            "year":      str(file_date.year),
            "month":     MONTH_NAMES[file_date.month],
        })

    print(f"\n  Analysis complete.\n")
    return file_list


# ── STEP 6: FIND DUPLICATES ──────────────────────────────────────────────────

def find_duplicates(file_list):
    """Group files by their fingerprint to find duplicates."""
    hash_map = defaultdict(list)
    for f in file_list:
        if f["hash"]:
            hash_map[f["hash"]].append(f)
    return {h: files for h, files in hash_map.items() if len(files) > 1}


# ── STEP 7: HANDLE DUPLICATES ────────────────────────────────────────────────

def handle_duplicates(duplicates):
    """
    For each group of duplicates, ask the user what to do.
    Returns a set of file paths to SKIP (don't move these).
    """
    skip_paths = set()

    if not duplicates:
        return skip_paths

    total_groups = len(duplicates)
    print(f"\n  ⚠️  Found {total_groups} group(s) of duplicate files.")
    print("  I'll ask you what to do with each group.\n")
    print("  " + "─" * 50)

    for i, (file_hash, files) in enumerate(duplicates.items(), 1):
        print(f"\n  DUPLICATE GROUP {i} of {total_groups}")
        print(f"  These {len(files)} files are identical:\n")

        for j, f in enumerate(files):
            size_kb = f["path"].stat().st_size / 1024
            print(f"    [{j+1}] {f['path']}  ({size_kb:.1f} KB)")

        print(f"\n  What do you want to do?")
        print(f"  1) Keep ALL of them (move all to sorted folders)")
        print(f"  2) Keep only the FIRST one, skip the rest")
        print(f"  3) Skip ALL of them (don't move any)")

        while True:
            choice = input("\n  Type 1, 2, or 3: ").strip()
            if choice in ["1", "2", "3"]:
                break
            print("  Please type 1, 2, or 3.")

        if choice == "2":
            # Skip everything except the first file
            for f in files[1:]:
                skip_paths.add(f["path"])
            print(f"  ✅ Will keep: {files[0]['path'].name}")
        elif choice == "3":
            # Skip all files in this group
            for f in files:
                skip_paths.add(f["path"])
            print(f"  ⏭️  Skipping all {len(files)} files.")
        else:
            print(f"  ✅ Will move all {len(files)} files.")

    return skip_paths


# ── STEP 8: PRINT THE PLAN ───────────────────────────────────────────────────

def print_plan(file_list, skip_paths, destination):
    """Show the user exactly what will happen before doing anything."""
    print(f"\n  {'─' * 50}")
    print(f"  MOVE PLAN — Here's what will happen:\n")

    move_count = 0
    for f in file_list:
        if f["path"] in skip_paths:
            continue
        dest = Path(destination) / f["year"] / f["month"] / f["category"] / f["new_name"]
        print(f"  {f['path'].name}")
        print(f"    → {dest}")
        move_count += 1

    print(f"\n  Total files to move: {move_count}")
    print(f"  Total files to skip: {len(skip_paths)}")
    print(f"  {'─' * 50}\n")


# ── STEP 9: GENERATE REPORT ──────────────────────────────────────────────────

def generate_report(file_list, skip_paths, destination, dry_run):
    """Write a text report of everything that was (or would be) moved."""
    report_path = Path(destination) / "sort_report.txt"
    mode = "PREVIEW" if dry_run else "COMPLETED"

    lines = [
        "====================================================",
        f"  SOUTHDREAMS PHOTO SORTER v2.0 — {mode} REPORT",
        f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Destination: {destination}",
        "====================================================\n",
    ]

    moved = []
    skipped = []

    for f in file_list:
        dest = Path(destination) / f["year"] / f["month"] / f["category"] / f["new_name"]
        if f["path"] in skip_paths:
            skipped.append(f"  SKIPPED: {f['path']}")
        else:
            moved.append(f"  MOVED: {f['path']}\n      → {dest}")

    lines.append(f"FILES MOVED ({len(moved)}):\n")
    lines.extend(moved)
    lines.append(f"\nFILES SKIPPED ({len(skipped)}):\n")
    lines.extend(skipped)

    # Don't write the file in dry run, just print to screen
    if not dry_run:
        os.makedirs(destination, exist_ok=True)
        with open(report_path, "w") as f:
            f.write("\n".join(lines))
        print(f"\n  📄 Report saved to: {report_path}")
    else:
        print("\n  📄 (Report will be saved after running with --confirm)\n")


# ── STEP 10: DO THE ACTUAL MOVE ──────────────────────────────────────────────

def sort_files(file_list, skip_paths, destination):
    """Move all the files into their new sorted folders."""
    moved_count = 0
    error_count = 0

    print("\n  Moving files...\n")

    for f in file_list:
        if f["path"] in skip_paths:
            continue

        dest_folder = Path(destination) / f["year"] / f["month"] / f["category"]
        dest_file   = dest_folder / f["new_name"]

        try:
            os.makedirs(dest_folder, exist_ok=True)

            # If a file with the same name already exists at destination, add a number
            counter = 1
            while dest_file.exists():
                stem = Path(f["new_name"]).stem
                ext  = Path(f["new_name"]).suffix
                dest_file = dest_folder / f"{stem}_{counter}{ext}"
                counter += 1

            shutil.move(str(f["path"]), str(dest_file))
            moved_count += 1
            print(f"  ✅ {f['path'].name} → {dest_file.relative_to(destination)}")

        except (OSError, PermissionError) as e:
            error_count += 1
            print(f"  ❌ FAILED: {f['path'].name} — {e}")

    print(f"\n  Done! Moved {moved_count} file(s). Errors: {error_count}\n")


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="SouthDreams Photo Sorter v2.0 — Sort photos by Year/Month/Type.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("source",      help="Folder containing your unsorted photos")
    parser.add_argument("destination", help="Folder where sorted photos will go")
    parser.add_argument("--confirm",   action="store_true", help="Actually move the files (default is preview only)")
    parser.add_argument("--no-rename", action="store_true", help="Don't rename files to their date")

    args = parser.parse_args()
    dry_run = not args.confirm

    print("""
====================================================
  SOUTHDREAMS PHOTO SORTER v2.0
  by SouthDreams | Dirty Road Creations
  github.com/southdreams
====================================================
    """)

    if not PILLOW_AVAILABLE:
        print("  ⚠️  Pillow is not installed. EXIF dates won't be read.")
        print("  Install it with: pip install Pillow")
        print("  Falling back to file modified dates.\n")

    # Scan
    file_list = scan_folder(args.source)
    if not file_list:
        return

    # Find duplicates and ask user
    duplicates = find_duplicates(file_list)
    skip_paths = handle_duplicates(duplicates)

    # Show the plan
    print_plan(file_list, skip_paths, args.destination)

    # Generate report
    generate_report(file_list, skip_paths, args.destination, dry_run)

    if dry_run:
        print("  🛡️  SAFE MODE is ON. Nothing was moved.")
        print("  Run with --confirm to actually sort your files.\n")
        return

    # Do it
    sort_files(file_list, skip_paths, args.destination)
    generate_report(file_list, skip_paths, args.destination, dry_run=False)


if __name__ == "__main__":
    main()
