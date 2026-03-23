# Text Editor (Tkinter)

A simple desktop text editor built with Python and Tkinter.

## Features

- Open files (`.txt`, `.c`, `.py`)
- Edit text in a large text area
- Save files (`.txt`, `.c`, `.py`)
- Shows the currently opened/saved file path in the window title

## Project Structure

- `main(notebook).py` — main application script
- `README.md` — project documentation

## Requirements

- Python 3
- Tkinter (usually included with Python)

If Tkinter is missing on Linux, install it using your distro package manager (for example, `python3-tk` on Debian/Ubuntu).

## Run the App

From the project folder, run:

```bash
python3 "main(notebook).py"
```

## How to Use

1. Click **Open folder** to open a file.
2. Edit content in the text area.
3. Click **Save** to save content to a file.

## Notes

- The app currently uses two buttons: **Save** and **Open folder**.
- The **Open folder** button opens a file picker (not a folder picker).

## Linux build (manual)

To build a Linux app binary manually:

1. Run the build script:

```bash
chmod +x build_linux.sh
./build_linux.sh
```

2. Output files are created in `dist/`:
	- `text-editor` (Linux executable)
	- `text-editor.desktop` (desktop launcher)

3. Optional: add launcher to app menu:

```bash
cp dist/text-editor.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications 2>/dev/null || true
```

The app icon uses `noteBook.png` on Linux.
