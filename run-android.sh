#!/data/data/com.termux/files/usr/bin/bash
# ====================================================
#   SOUTHDREAMS PHOTO SORTER v2.0 — Android Launcher
#   by SouthDreams | Dirty Road Creations
# ====================================================

clear

echo ""
echo "===================================================="
echo "  SOUTHDREAMS PHOTO SORTER v2.0"
echo "  by SouthDreams | Dirty Road Creations"
echo "===================================================="
echo ""

# ── CHECK: Python installed? ─────────────────────────
if ! command -v python3 &> /dev/null; then
    echo "  Python3 not found. Installing now..."
    pkg update -y && pkg install python -y
fi

# ── CHECK: Pillow installed? ─────────────────────────
python3 -c "from PIL import Image" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "  Installing Pillow (needed to read photo dates)..."
    pip install Pillow --quiet
    echo "  Pillow installed."
    echo ""
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── ASK: Source folder ───────────────────────────────
echo "  Where are your UNSORTED photos?"
echo ""
echo "  Examples:"
echo "    /sdcard/DCIM"
echo "    /sdcard/Pictures"
echo "    /sdcard/Download"
echo ""
read -rp "  Type or paste the folder path: " SOURCE

if [ ! -d "$SOURCE" ]; then
    echo "  [ERROR] Folder not found: $SOURCE"
    read -rp "  Press Enter to close..."
    exit 1
fi

# ── ASK: Destination folder ──────────────────────────
echo ""
echo "  Where do you want the SORTED photos to go?"
echo ""
echo "  Example: /sdcard/Sorted_Photos"
echo ""
read -rp "  Type or paste the destination path: " DEST

echo ""

# ── ASK: Mode ────────────────────────────────────────
echo "  What do you want to do?"
echo ""
echo "  1) PREVIEW — Show me what will happen (safe, nothing moves)"
echo "  2) SORT    — Actually sort and move the files"
echo ""
read -rp "  Type 1 or 2: " CHOICE

echo ""

if [ "$CHOICE" = "2" ]; then
    echo "  Running in SORT mode..."
    python3 "$SCRIPT_DIR/src/photo_sorter.py" "$SOURCE" "$DEST" --confirm
else
    echo "  Running in PREVIEW mode (safe)..."
    python3 "$SCRIPT_DIR/src/photo_sorter.py" "$SOURCE" "$DEST"
fi

echo ""
read -rp "  Press Enter to close..."
