# 📷 SouthDreams Photo Sorter v2.0
### by [SouthDreams](https://github.com/southdreams) | Dirty Road Creations

> *"Built dirty. Works clean."*

---

## What It Does

**SouthDreams Photo Sorter** takes a messy folder full of photos, videos, and camera files and automatically organizes them into a clean, logical structure — sorted by **Year, Month, and File Type**. No subscriptions. No cloud. Your files never leave your machine.

**Before:**
```
Downloads/
├── IMG_4821.jpg
├── VID_20240315.mp4
├── screenshot_home.png
├── DSC_0042.CR2
├── IMG_4821_copy.jpg   ← duplicate!
└── random_photo.jpeg
```

**After:**
```
Sorted_Photos/
└── 2024/
    └── March/
        ├── Photos/
        │   ├── 2024-03-15_IMG_4821.jpg
        │   └── 2024-03-15_random_photo.jpeg
        ├── Videos/
        │   └── 2024-03-15_VID_20240315.mp4
        ├── Screenshots/
        │   └── 2024-03-15_screenshot_home.png
        └── RAW/
            └── 2024-03-15_DSC_0042.CR2
```

---

## Features

- ✅ **Sorts by Year / Month / File Type** — clean folder structure every time
- ✅ **Reads EXIF data** — uses the actual date the photo was *taken*, not when it was copied
- ✅ **Renames files to their date** — `2024-03-15_IMG_4821.jpg`
- ✅ **Duplicate detection** — finds identical files and *asks you* what to do
- ✅ **RAW camera support** — handles CR2, CR3, NEF, ARW, DNG, ORF, RW2 and more
- ✅ **Screenshot detection** — screenshots go to their own folder
- ✅ **Generates a full report** — a text file showing everything that moved
- ✅ **Safe preview mode** — see the full plan before a single file moves
- ✅ **Windows + Android** — launchers included for both platforms
- ✅ **100% local** — your photos never leave your computer

---

## Requirements

- Python 3.7 or newer
- Pillow library (for reading photo dates — the launcher installs this for you automatically)

To check your Python version:
```bash
python --version
```

---

## How To Use It

---

### 🤖 Android (Termux)

**First time only:**
```bash
chmod +x run-android.sh && ./run-android.sh
```

**Every time after:**
```bash
./run-android.sh
```

The script installs everything it needs automatically, then walks you through the rest.

---

### 🪟 Windows

1. Make sure [Python](https://www.python.org/downloads/) is installed
   - During install, check **"Add Python to PATH"**
2. Open the `Southdreams-Photo-Sorter` folder
3. **Double-click `run-windows.bat`**
4. Follow the prompts — it installs Pillow automatically if needed

---

### ⚙️ Advanced / Manual Usage

**Preview mode (safe — nothing moves):**
```bash
python src/photo_sorter.py /path/to/messy/photos /path/to/sorted/destination
```

**Actually sort the files:**
```bash
python src/photo_sorter.py /path/to/messy/photos /path/to/sorted/destination --confirm
```

**Sort without renaming files:**
```bash
python src/photo_sorter.py /path/to/source /path/to/dest --confirm --no-rename
```

---

## Supported File Types

| Category    | Extensions |
|-------------|------------|
| Photos      | .jpg .jpeg .png .gif .bmp .webp .heic .tiff |
| Videos      | .mp4 .mov .avi .mkv .wmv .flv .m4v .3gp .mts |
| RAW         | .cr2 .cr3 .nef .arw .dng .orf .rw2 .pef .raf |
| Screenshots | .png (with "screenshot" in filename) |
| Other       | Everything else |

---

## Duplicate Files

When the sorter finds two or more identical files it will stop and ask you:

```
  DUPLICATE GROUP 1 of 2
  These 2 files are identical:

    [1] /Downloads/IMG_4821.jpg  (2,341.4 KB)
    [2] /Downloads/IMG_4821_copy.jpg  (2,341.4 KB)

  What do you want to do?
  1) Keep ALL of them
  2) Keep only the FIRST one, skip the rest
  3) Skip ALL of them
```

You stay in control. Nothing gets deleted without your input.

---

## The Report

After sorting, a `sort_report.txt` file is saved in your destination folder showing every file that moved and where it went. Great for double-checking nothing was missed.

---

## FAQ

**Will it delete my original files?**
No. It *moves* them, not copies. Your originals go to the new sorted location. Run in preview mode first if you're unsure.

**What if two files have the same name at the destination?**
It adds a number automatically. Example: `2024-03-15_photo.jpg` becomes `2024-03-15_photo_1.jpg`.

**Does it work on Termux (Android)?**
Yes. Tested on Termux. Point it at your SD card.

**What if Pillow isn't installed?**
The launcher installs it for you. If you're running manually, run `pip install Pillow` first.

---

## License

MIT License — free to use, modify, and distribute.
Credit appreciated but not required.

---

## About

**Dirty Road Creations** is a brand under **SouthDreams** — building real tools from salvaged tech and open source software.

- 🌐 GitHub: [github.com/southdreams](https://github.com/southdreams)

---

*Built by Iron & Ink | Dirty Road Creations*
*We help the ones the world tries to forget.*
