"""Task 2 - Desktop file organizer.

Usage:
    python organizer.py                 # organizes ~/Downloads
    python organizer.py /path/to/folder
    python organizer.py /path --dry-run # preview only
"""
import argparse
import os
import shutil
from collections import Counter
from pathlib import Path

EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents", ".txt": "Documents",
    ".xls": "Documents", ".xlsx": "Documents", ".ppt": "Documents", ".pptx": "Documents",
    ".csv": "Documents", ".odt": "Documents",
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
    ".bmp": "Images", ".svg": "Images", ".webp": "Images",
    # Videos
    ".mp4": "Videos", ".mkv": "Videos", ".avi": "Videos", ".mov": "Videos", ".wmv": "Videos",
    # Archives
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives", ".tar": "Archives", ".gz": "Archives",
    # Code
    ".py": "Code", ".js": "Code", ".html": "Code", ".css": "Code", ".java": "Code",
    ".c": "Code", ".cpp": "Code", ".json": "Code", ".sql": "Code",
}
OTHERS = "Others"


def unique_path(dest: Path) -> Path:
    """Return a non-colliding path: file.txt -> file (1).txt -> file (2).txt"""
    if not dest.exists():
        return dest
    i = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({i}){dest.suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def organize(folder: Path, dry_run: bool = False):
    moved = Counter()
    errors = []
    skipped = 0

    with os.scandir(folder) as it:
        entries = [e for e in it if e.is_file()]

    for entry in entries:
        src = Path(entry.path)
        if src.resolve() == Path(__file__).resolve():
            skipped += 1  # never move this script itself
            continue

        category = EXTENSION_MAP.get(src.suffix.lower(), OTHERS)
        target_dir = folder / category
        try:
            if not dry_run:
                target_dir.mkdir(exist_ok=True)  # create category folder dynamically
            dest = unique_path(target_dir / src.name)
            if dry_run:
                print(f"[dry-run] {src.name} -> {category}/{dest.name}")
            else:
                shutil.move(str(src), str(dest))
            moved[category] += 1
        except PermissionError:
            errors.append((src.name, "Permission denied"))
        except FileExistsError:
            errors.append((src.name, "File already exists"))
        except OSError as e:
            errors.append((src.name, str(e)))

    print_summary(folder, moved, errors, skipped, dry_run)


def print_summary(folder, moved, errors, skipped, dry_run):
    total = sum(moved.values())
    print("\n" + "=" * 40)
    print(" ORGANIZER SUMMARY" + (" (DRY RUN)" if dry_run else ""))
    print("=" * 40)
    print(f" Folder        : {folder}")
    print(f" Files moved   : {total}")
    for cat, n in sorted(moved.items()):
        print(f"   - {cat:<10}: {n}")
    print(f" Skipped       : {skipped}")
    print(f" Errors        : {len(errors)}")
    for name, reason in errors:
        print(f"   ! {name}: {reason}")
    print("=" * 40)


def main():
    parser = argparse.ArgumentParser(description="Organize files into category subfolders.")
    parser.add_argument("folder", nargs="?", default=str(Path.home() / "Downloads"))
    parser.add_argument("--dry-run", action="store_true", help="show what would happen without moving")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser()
    if not folder.is_dir():
        print(f"Error: '{folder}' is not a valid folder.")
        return
    organize(folder, args.dry_run)


if __name__ == "__main__":
    main()
