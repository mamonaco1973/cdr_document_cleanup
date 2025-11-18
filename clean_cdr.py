#!/usr/bin/python3

import os
import shutil
import argparse

# ==============================================================================
# Function: move_files_to_documents
# Purpose:
#   - Scan <root>/cdr/data for directories containing loose files.
#   - Move loose files into a "Documents" folder in the same directory.
#   - Support dry-run (default) and execution mode (-execute).
# Notes:
#   - Only files directly under a directory are moved.
#   - ".empty" placeholder files are ignored.
#   - Existing filenames are preserved; collisions receive numeric suffixes.
# ==============================================================================

def move_files_to_documents(root, execute=False):
    """
    Core logic for scanning and relocating files into Documents folders.
    """

    scan_root = os.path.join(root, "cdr", "data")

    # Validate the scan root path exists
    if not os.path.isdir(scan_root):
        raise SystemExit(f"ERROR: Path does not exist: {scan_root}")

    print(f"Scanning: {scan_root}")
    print(f"Mode: {'EXECUTION' if execute else 'DRY-RUN'}")
    print("-" * 80)

    # Walk the directory tree under cdr/data
    for dirpath, dirnames, filenames in os.walk(scan_root, topdown=True):

        # Prevent descent into existing Documents folders
        dirnames[:] = [d for d in dirnames if d.lower() != "documents"]

        # Identify real files (ignore .empty placeholders)
        files_here = [
            f for f in filenames
            if f != ".empty" and os.path.isfile(os.path.join(dirpath, f))
        ]

        # Skip directories with no direct files
        if not files_here:
            continue

        documents_dir = os.path.join(dirpath, "Documents")

        # Create Documents directory if needed
        if not os.path.exists(documents_dir):
            print(f"[CREATE] {documents_dir}")
            if execute:
                os.makedirs(documents_dir, exist_ok=True)

        # Process each file present in the directory
        for fname in files_here:
            src = os.path.join(dirpath, fname)
            dst = os.path.join(documents_dir, fname)

            # Handle name collisions with numeric suffixing
            if os.path.exists(dst):
                base, ext = os.path.splitext(fname)
                counter = 1
                while True:
                    newname = f"{base}_{counter}{ext}"
                    dst2 = os.path.join(documents_dir, newname)
                    if not os.path.exists(dst2):
                        dst = dst2
                        break
                    counter += 1

            print(f"[MOVE] {src} -> {dst}")

            # Perform file move only when executed with -execute
            if execute:
                shutil.move(src, dst)


# ==============================================================================
# Function: main
# Purpose:
#   - Parse CLI arguments.
#   - Normalize the root path.
#   - Invoke the file relocation routine.
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Move loose files into Documents/ subfolders."
    )

    parser.add_argument(
        "-root",
        default=".",
        help="Root directory containing cdr/data (default: .)"
    )

    parser.add_argument(
        "-execute",
        action="store_true",
        help="Perform file moves. Without this flag, only a dry-run occurs."
    )

    args = parser.parse_args()

    # Normalize root path and expand tildes
    root = os.path.abspath(os.path.expanduser(args.root))

    # Execute the main file-moving logic
    move_files_to_documents(root, execute=args.execute)


# ==============================================================================
# Script entry point
# ==============================================================================

if __name__ == "__main__":
    main()
