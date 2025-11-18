# clear_cdr.py — CDR Directory Normalization Utility

## Overview

`clear_cdr.py` is a cleanup and normalization tool designed for CDR-style
(Clinical Data Repository) directory exports. These exports often contain
deeply nested directory trees representing **products**, **studies**, and
standard subfolders such as:

- `Analyis/`
- `Collaboration/`
- `Data/`
- `Documents/`
- `Share/`

However, depending on the originating system, files may appear **directly
within a study directory**, rather than inside the intended `Documents/`
subfolder. This script corrects that structure by relocating those files into
a consistent and expected location.

The script is **safe by default**, performing a dry-run unless explicitly
executed with the `-execute` flag.

---

## Default Directory Structure

Below is the typical structure found under the CDR export root:

```
cdr/
  data/
    <drive or source>/
      <product>/
        <study>/
          Analyis/
          Collaboration/
          Data/
          Documents/
          Share/
          <loose files that should be moved>...
```

### Example

```
cdr/data/driveA/alpha/CBS/
  Analyis/
  Collaboration/
  Data/
  Documents/
  Share/
  da47079f565b4fd4.docx
  da47079f565b4fd4.pdf
  da47079f565b4fd4.txt
  da47079f565b4fd4.xlsx
```

After running the script in **execute mode**, the result will be:

```
cdr/data/driveA/alpha/CBS/
  Analyis/
  Collaboration/
  Data/
  Documents/
    da47079f565b4fd4.docx
    da47079f565b4fd4.pdf
    da47079f565b4fd4.txt
    da47079f565b4fd4.xlsx
  Share/
```

---

## What the Script Does

`clear_cdr.py` performs the following tasks:

1. Accepts a **root directory** (default: current working directory).
2. Locates the path `<root>/cdr/data`.
3. Recursively scans all subdirectories under `cdr/data/`.
4. For each directory:
   - Identifies files located **directly inside the directory** (not inside
     subfolders).
   - Ignores placeholder files such as `.empty`.
   - Ensures a `Documents/` folder exists in that directory.
   - Moves the loose files into the `Documents/` folder.
   - Applies collision-safe renaming (e.g., `file_1.docx`) if needed.
5. By default, performs a **dry run** (prints actions without making changes).
6. If run with `-execute`, it performs the actual file moves.

This script operates without assumptions about the drive name or hierarchy.
Any structure under `cdr/data` is processed uniformly.

---

## Script Parameters

### `-root <path>`

Specifies the top-level directory that contains the `cdr/` folder.

- **Default:** `.` (current working directory)
- The script will scan:

```
<root>/cdr/data
```

**Examples:**

```
.\clear_cdr.py -root /tmp
.\clear_cdr.py -root /
```

---

### `-execute`

When present, the script will **perform actual file moves**.

If omitted, the script operates in **dry-run mode**, printing what would be
moved without modifying the directory tree.

**Examples:**

Dry run (default):

```
.\clear_cdr.py -root /
```

Live execution:

```
.\clear_cdr.py -root / -execute
```

---

## Safety Features

- **Dry-run first:** No moves occur unless `-execute` is supplied.
- **Collision avoidance:** Files with duplicate names receive a numeric suffix.
- **Directory protection:** Existing `Documents/` folders are not reprocessed.
- **Idempotent:** Running the script multiple times produces consistent results.

---

## When to Use This Script

Use `clear_cdr.py` when:

- You receive CDR exports with inconsistent file placement.
- Studies contain loose files mixed with folders.
- You need predictable downstream folder structures.
- You want a safe, repeatable way to normalize multiple CDR datasets.

---

## Example Workflows

### Normalize a CDR export inside `/fsx/cdr`:

```
.\clear_cdr.py -root /fsx -execute
```

### Validate what would happen without changing anything:

```
.\clear_cdr.py -root /fsx
```

