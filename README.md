# Note Book

A modern desktop text editor built with Python + CustomTkinter.

## Features

- Fast file open and save
- File type support: `.txt`, `.py`, `.c`, `.html`, `.css`, `.js`
- Clean formatting toolbar:
  - Bold and Italic
  - Text alignment (Left, Center, Right)
  - Font family selector
  - Font size selector
- Smart font behavior:
  - Existing text keeps the style it already had
  - Newly typed text follows the currently selected font settings
- Theme switcher: Light / Dark / System
- Live status bar: line, column, character count, and word count
- Smooth zoom animation for keyboard and mouse zoom actions
- Zoom step behavior: each action changes zoom by exactly 10%
- Zoom limits: minimum 100% (normal) and maximum 300%
- Zoom shortcuts:
  - `Ctrl + +` to zoom in
  - `Ctrl + -` to zoom out
  - `Ctrl + Mouse Wheel` (and Linux wheel buttons) to zoom
- Formatting shortcuts:
  - `Ctrl + B` for Bold
  - `Ctrl + I` for Italic
- Undo and redo support:
  - Undo: `Ctrl + Z`
  - Redo: `Ctrl + Y` and `Ctrl + Shift + Z`
- Unsaved changes protection:
  - Prompts when closing the window with unsaved edits
  - Prompts when opening another file with unsaved edits
  - Save / Don't Save / Cancel flow
- File dialog quality-of-life:
  - Starts in `Documents` by default (falls back to Home)
  - Remembers the last used folder for next open/save
- Responsive editor layout
- Custom app name and icon

## Requirements

- Python 3
- `customtkinter`
- Tkinter (normally included with Python)

Install dependency:

```bash
python3 -m pip install customtkinter
```

## Run

```bash
python3 "main(notebook).py"
```

## Usage

1. Click **Open folder** to open a file.
2. Edit content in the text area.
3. Use the top toolbar for bold, italic, alignment, font family, and font size.
4. Click **Save** to save changes.
5. Use zoom controls (`Ctrl + +`, `Ctrl + -`, or `Ctrl + Mouse Wheel`) when needed.
6. Use mode selector to switch theme.

## Manual Linux Build

```bash
chmod +x build_linux.sh
./build_linux.sh
```

Build output:

- `dist/NoteBook` (Linux executable)
- `dist/NoteBook.desktop` (desktop launcher)

Optional: add launcher to app menu

```bash
cp dist/NoteBook.desktop ~/.local/share/applications/notebook.desktop
chmod +x ~/.local/share/applications/notebook.desktop
update-desktop-database ~/.local/share/applications 2>/dev/null || true
```
Note Book Icon: 
![Note Book Logo](assets/icon-img.png)

Note Book Preview:
![Note Book Application Preview](assets/preview-image(note-book).png)
