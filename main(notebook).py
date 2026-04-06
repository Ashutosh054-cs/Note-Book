import customtkinter 
import os
import shutil
import subprocess
import sys
import tkinter.font as tkfont
from tkinter import END, INSERT, PhotoImage, TclError, filedialog
from formatting_toolbar import create_formatting_toolbar

#Code for custom tkinter :
#we will use custom tkinter to toggle between dark and light mode which using the system user preference
#we will select the default mode what user had
customtkinter.set_appearance_mode("System")

MIN_FONT_SIZE = 12
MAX_FONT_SIZE = 36
FONT_STEP = 2
MIN_ZOOM_PERCENT = 50
MAX_ZOOM_PERCENT = 300
ZOOM_STEP_PERCENT = 10
PAPER_TINT = "#FEF9E7"
TEXT_COLOR = "#333333"
SELECTION_BG = "#BFD6FF"
SELECTION_FG = "#1F2A44"
BUNDLED_FONT_DIR = "assets/fonts"
FONT_FILE_EXTENSIONS = (".ttf", ".otf")
PREFERRED_FONT_FAMILIES = [
    "QEDaveMergens",
    "QEGHHughes",
    "QEPhillips",
]

#function for custom tkinter mode:
def toggle_mode(new_toggle_mode):
    customtkinter.set_appearance_mode(new_toggle_mode)

def save_file(screen , text_edit):
    filepath = filedialog.asksaveasfilename(
        filetypes=[
            ("Text Files" , "*.txt"),
            ("C program" , "*.c"),
            ("Python program" , "*.py"),
            ("HTML file" , "*.html"),
            ("CSS file " ,"*.css"),
            ("js file", "*.js"),
        ]
    )

    if not filepath:
        return
    
    with open(filepath, "w", encoding="utf-8") as f:
        content = text_edit.get("1.0", "end-1c")
        f.write(content) 

    screen.title(f"filepath: {filepath}")


def open_file(screen , text_edit):
    filepath = filedialog.askopenfilename(
        filetypes=[
            ("Text Files" , "*.txt"),
            ("C program" , "*.c"),
            ("Python program" , "*.py"),
            ("HTML file" , "*.html"),
            ("CSS file ","*.css"),
            ("js file", "*.js"),
        ]
    )

    if not filepath:
        return
    
    text_edit.delete("1.0", END)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        text_edit.insert(END, content)

    screen.title(f"filepath: {filepath}")


def update_status_bar(text_edit , status_bar):
    line , col = text_edit.index(INSERT).split(".")
    content = text_edit.get("1.0" , "end-1c")
    chars = len(content)
    words = len(content.split())
    status_bar.configure(text=f"Line: {int(line)}   Col: {int(col) + 1}   Chars: {chars}   Words: {words}")


def get_asset_path(filename):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)


def get_bundled_font_files():
    font_dir = get_asset_path(BUNDLED_FONT_DIR)
    if not os.path.isdir(font_dir):
        return []

    font_files = []
    for name in os.listdir(font_dir):
        lower_name = name.lower()
        if lower_name.endswith(FONT_FILE_EXTENSIONS):
            font_files.append(os.path.join(font_dir, name))

    return sorted(font_files)


def install_bundled_fonts():
    font_files = get_bundled_font_files()
    if not font_files:
        return False

    target_dir = os.path.expanduser("~/.local/share/fonts/NoteBook")
    os.makedirs(target_dir, exist_ok=True)

    copied_any = False
    for source_path in font_files:
        target_path = os.path.join(target_dir, os.path.basename(source_path))
        if (not os.path.exists(target_path)) or (os.path.getsize(source_path) != os.path.getsize(target_path)):
            shutil.copy2(source_path, target_path)
            copied_any = True

    cache_command = shutil.which("fc-cache")
    if cache_command and copied_any:
        try:
            subprocess.run([cache_command, "-f", target_dir], check=False, capture_output=True)
        except OSError:
            pass

    return True


def get_bundled_font_family_candidates():
    candidates = []
    seen = set()
    for font_path in get_bundled_font_files():
        family_name = os.path.splitext(os.path.basename(font_path))[0].strip()
        key = family_name.lower()
        if family_name and key not in seen:
            seen.add(key)
            candidates.append(family_name)
    return candidates


def set_app_icon(screen):
    try:
        icon_path = get_asset_path("noteBook.png")
        icon_image = PhotoImage(file=icon_path)
        screen.iconphoto(True, icon_image)
        screen._icon_image = icon_image
    except TclError:
        pass


def freeze_existing_text_font(text_edit, family, size):
    tk_text = text_edit._textbox if hasattr(text_edit, "_textbox") else text_edit
    end_index = tk_text.index("end-1c")
    if end_index == "1.0":
        return

    # Preserve currently written content with a concrete font tag before
    # changing the base editor font, so new font affects only new typing.
    safe_family = family.replace(" ", "_")
    font_tag = f"base_font_{safe_family}_{size}"
    frozen_font = tkfont.Font(family=family, size=size)
    tk_text.tag_config(font_tag, font=frozen_font)
    tk_text.tag_add(font_tag, "1.0", end_index)
    tk_text.tag_lower(font_tag)
    return font_tag, frozen_font


def get_scaled_font_size(base_size, zoom_percent):
    return max(1, int(round(base_size * zoom_percent / 100)))


def normalize_font_name(name):
    return "".join(ch for ch in name.lower() if ch.isalnum())


def build_available_font_maps():
    available = sorted(set(tkfont.families()), key=lambda name: name.lower())
    by_lower = {}
    by_normalized = {}

    for family in available:
        lowered = family.lower()
        normalized = normalize_font_name(family)
        by_lower.setdefault(lowered, family)
        by_normalized.setdefault(normalized, family)

    return available, by_lower, by_normalized


def resolve_installed_font_family(candidate, by_lower, by_normalized):
    if not candidate:
        return None

    direct = by_lower.get(candidate.lower())
    if direct:
        return direct

    return by_normalized.get(normalize_font_name(candidate))


def get_fontconfig_family_aliases():
    aliases = {}
    fc_scan = shutil.which("fc-scan")
    if not fc_scan:
        return aliases

    for font_path in get_bundled_font_files():
        stem = os.path.splitext(os.path.basename(font_path))[0].strip()
        if not stem:
            continue

        try:
            result = subprocess.run(
                [fc_scan, "--format=%{family}\\n", font_path],
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError:
            continue

        if result.returncode != 0:
            continue

        first_line = (result.stdout or "").strip().splitlines()
        if not first_line:
            continue

        family_name = first_line[0].split(",")[0].strip()
        if family_name:
            aliases[stem] = family_name

    return aliases


def get_default_font_family():
    _available, by_lower, by_normalized = build_available_font_maps()
    candidate_families = PREFERRED_FONT_FAMILIES + get_bundled_font_family_candidates()

    for candidate in candidate_families:
        resolved = resolve_installed_font_family(candidate, by_lower, by_normalized)
        if resolved:
            return resolved
    return "Helvetica"


def get_font_family_options(default_family, fontconfig_aliases):
    _available, by_lower, by_normalized = build_available_font_maps()
    candidate_families = PREFERRED_FONT_FAMILIES
    options = []
    option_to_family = {}
    seen = set()

    def add_option(label, resolved_family):
        key = label.lower()
        if key in seen:
            return
        seen.add(key)
        options.append(label)
        option_to_family[label] = resolved_family

    for candidate in candidate_families:
        resolved = resolve_installed_font_family(candidate, by_lower, by_normalized)
        if not resolved:
            alias_candidate = fontconfig_aliases.get(candidate)
            if alias_candidate:
                resolved = resolve_installed_font_family(alias_candidate, by_lower, by_normalized)
        if resolved:
            add_option(candidate, resolved)
        else:
            # Keep user-provided fonts visible in menu. They may become
            # available after font cache refresh or app restart.
            add_option(candidate, candidate)

    add_option(default_family, default_family)

    helvetica = resolve_installed_font_family("Helvetica", by_lower, by_normalized)
    if helvetica:
        add_option("Helvetica", helvetica)

    if not options:
        fallback = resolve_installed_font_family("TkDefaultFont", by_lower, by_normalized) or "Helvetica"
        add_option(fallback, fallback)

    return options, option_to_family


def main():
    screen = customtkinter.CTk()
    screen.title("Note Book")
    set_app_icon(screen)
    screen.rowconfigure(0, weight=0)
    screen.rowconfigure(1, weight=1)
    screen.rowconfigure(2, weight=0)
    screen.columnconfigure(0, weight=0)
    screen.columnconfigure(1, weight=1)
    screen.minsize(900, 550)

    install_bundled_fonts()
    fontconfig_aliases = get_fontconfig_family_aliases()

    editor_frame = customtkinter.CTkFrame(screen)
    editor_frame.grid(row=1, column=1, sticky="nsew", padx=(8, 10), pady=(6, 6))
    editor_frame.rowconfigure(0, weight=1)
    editor_frame.columnconfigure(0, weight=1)
    editor_frame.columnconfigure(1, weight=0)

    font_state = {"size": 18, "family": get_default_font_family()}
    zoom_state = {"percent": 100}
    current_font_size = {"value": font_state["size"]}
    frozen_base_fonts = {}
    _font_list, available_by_lower, available_by_normalized = build_available_font_maps()

    def get_display_font_size():
        return get_scaled_font_size(font_state["size"], zoom_state["percent"])

    #font will be replaced by the value passed on from option_font
    font = customtkinter.CTkFont(family=font_state["family"] , size=get_display_font_size())

    text_edit = customtkinter.CTkTextbox(
        editor_frame,
        wrap="word",
        fg_color=PAPER_TINT,
        text_color=TEXT_COLOR,
        border_width=0,
        corner_radius=0,
        font=font,
        undo=True,
    )

    #Wrap ="none " will wont alloww to break the line , but warp="word " will help to break the line
    text_edit.grid(row=0, column=0, sticky="nsew")

    scrollbar = customtkinter.CTkScrollbar(editor_frame , orientation="vertical")
    scrollbar.grid(row=0, column=1, sticky="ns")

    status_bar = customtkinter.CTkLabel(screen , text="Line: 1   Col: 1   Chars: 0   Words: 0" ,
                          anchor="w")
    status_bar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

    
    notebook_refresh_job = {"id": None}

    def apply_notebook_style():
        tk_text = text_edit._textbox if hasattr(text_edit, "_textbox") else text_edit

        tk_text.configure(
            background=PAPER_TINT,
            foreground=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            selectbackground=SELECTION_BG,
            selectforeground=SELECTION_FG,
        )

        tk_text.tag_config("notebook_margin", lmargin1=22, lmargin2=22)
        tk_text.tag_add("notebook_margin", "1.0", "end-1c")

        tk_text.tag_lower("notebook_margin")

    def schedule_notebook_refresh():
        if notebook_refresh_job["id"] is not None:
            screen.after_cancel(notebook_refresh_job["id"])
        notebook_refresh_job["id"] = screen.after(35, run_notebook_refresh)

    def run_notebook_refresh():
        notebook_refresh_job["id"] = None
        apply_notebook_style()

    def refresh_editor_ui(event=None):
        update_status_bar(text_edit , status_bar)
        schedule_notebook_refresh()

    def apply_font_size(new_size):
        clamped_size = max(MIN_FONT_SIZE, min(MAX_FONT_SIZE, int(new_size)))
        previous_family = font_state["family"]
        previous_size = font_state["size"]

        tag_name, frozen_font = freeze_existing_text_font(
            text_edit,
            previous_family,
            get_scaled_font_size(previous_size, zoom_state["percent"]),
        )
        frozen_base_fonts[tag_name] = {"font": frozen_font, "base_size": previous_size}

        current_font_size["value"] = clamped_size
        font_state["size"] = clamped_size
        font.configure(size=get_display_font_size())
        font_size_label.configure(text=f"Text Size: {clamped_size}")
        toolbar_controls["set_size"](clamped_size)
        toolbar_controls["refresh_tag_fonts"]()

    def apply_font_family(new_family):
        mapped_family = font_option_to_family.get(new_family, new_family)
        resolved_family = resolve_installed_font_family(mapped_family, available_by_lower, available_by_normalized)
        if not resolved_family:
            resolved_family = resolve_installed_font_family(new_family, available_by_lower, available_by_normalized)
        if not resolved_family:
            return

        previous_family = font_state["family"]
        previous_size = font_state["size"]

        if resolved_family == previous_family:
            return

        tag_name, frozen_font = freeze_existing_text_font(
            text_edit,
            previous_family,
            get_scaled_font_size(previous_size, zoom_state["percent"]),
        )
        frozen_base_fonts[tag_name] = {"font": frozen_font, "base_size": previous_size}

        font_state["family"] = resolved_family
        font.configure(family=resolved_family)
        font.configure(size=get_display_font_size())
        toolbar_controls["set_family"](new_family)
        toolbar_controls["refresh_tag_fonts"]()

    font_family_values, font_option_to_family = get_font_family_options(font_state["family"], fontconfig_aliases)

    toolbar_frame, toolbar_controls = create_formatting_toolbar(
        screen,
        text_edit,
        font_state,
        apply_font_size,
        apply_font_family,
        font_family_values,
        get_display_font_size,
    )
    toolbar_frame.grid(row=0, column=1, sticky="ew", padx=(8, 10), pady=(10, 0))
    toolbar_controls["refresh_notebook_style"] = schedule_notebook_refresh

    def apply_zoom_percent(new_zoom_percent):
        clamped_zoom = max(MIN_ZOOM_PERCENT, min(MAX_ZOOM_PERCENT, int(new_zoom_percent)))
        if clamped_zoom == zoom_state["percent"]:
            return

        zoom_state["percent"] = clamped_zoom
        font.configure(size=get_display_font_size())

        for font_info in frozen_base_fonts.values():
            font_info["font"].configure(size=get_scaled_font_size(font_info["base_size"], clamped_zoom))

        toolbar_controls["refresh_tag_fonts"]()
        zoom_label.configure(text=f"Zoom: {clamped_zoom}%")

    def zoom_in(event=None):
        apply_zoom_percent(zoom_state["percent"] + ZOOM_STEP_PERCENT)
        schedule_notebook_refresh()
        return "break"

    def zoom_out(event=None):
        apply_zoom_percent(zoom_state["percent"] - ZOOM_STEP_PERCENT)
        schedule_notebook_refresh()
        return "break"

    tk_text = text_edit._textbox if hasattr(text_edit, "_textbox") else text_edit

    def undo_text(event=None):
        try:
            tk_text.edit_undo()
        except TclError:
            pass
        refresh_editor_ui()
        return "break"

    def redo_text(event=None):
        try:
            tk_text.edit_redo()
        except TclError:
            pass
        refresh_editor_ui()
        return "break"

    def handle_undo_redo_shortcuts(event):
        ctrl_pressed = bool(event.state & 0x4)
        shift_pressed = bool(event.state & 0x1)
        key = event.keysym.lower()

        if not ctrl_pressed:
            return None

        if key == "z" and not shift_pressed:
            return undo_text(event)

        if key == "y" or (key == "z" and shift_pressed):
            return redo_text(event)

        return None

    scrollbar.configure(command=text_edit.yview)
    text_edit.configure(yscrollcommand=scrollbar.set)

    #creating frame
    frame = customtkinter.CTkFrame(screen)
    frame.grid_columnconfigure(0, weight=1)
    save_btn = customtkinter.CTkButton(frame , text="Save" , command=lambda: save_file(screen ,  text_edit))
    def open_file_and_refresh():
        open_file(screen, text_edit)
        refresh_editor_ui()

    open_btn = customtkinter.CTkButton(frame , text="Open folder" , command=open_file_and_refresh)
    zoom_in_btn = customtkinter.CTkButton(frame, text="Zoom In (+)", command=zoom_in)
    zoom_out_btn = customtkinter.CTkButton(frame, text="Zoom Out (-)", command=zoom_out)
    font_size_label = customtkinter.CTkLabel(frame, text=f"Text Size: {current_font_size['value']}")
    zoom_label = customtkinter.CTkLabel(frame, text=f"Zoom: {zoom_state['percent']}%")
    save_btn.grid(row=0, column=0 , padx=10 , pady=(10, 6) , sticky="ew")
    open_btn.grid(row=1 , column=0 , padx=10 , pady=6 , sticky="ew")
    zoom_in_btn.grid(row=2, column=0, padx=10, pady=6, sticky="ew")
    zoom_out_btn.grid(row=3, column=0, padx=10, pady=6, sticky="ew")
    font_size_label.grid(row=4, column=0, padx=10, pady=(2, 6), sticky="w")
    zoom_label.grid(row=5, column=0, padx=10, pady=(0, 6), sticky="w")
    #Appereance mmode change code :
    option_toggle = customtkinter.CTkOptionMenu(frame , values=["Light" , "Dark" , "System"], command=toggle_mode)
    option_toggle.grid(row=6, column=0 , padx=10, pady=(6, 10) , sticky="ew")
    option_toggle.set("System")
    frame.grid(row=0,column=0 , rowspan=2, sticky="ns", padx=(10, 6), pady=(10, 6)) #ns = expand the frame to north and south

    text_edit.bind("<KeyRelease>" , refresh_editor_ui)
    text_edit.bind("<ButtonRelease-1>" , refresh_editor_ui)
    text_edit.bind("<MouseWheel>" , refresh_editor_ui)
    text_edit.bind("<Button-4>" , refresh_editor_ui)
    text_edit.bind("<Button-5>" , refresh_editor_ui)
    text_edit.bind("<Control-MouseWheel>", lambda event: zoom_in() if event.delta > 0 else zoom_out())
    text_edit.bind("<Control-Button-4>", zoom_in)
    text_edit.bind("<Control-Button-5>", zoom_out)
    tk_text.bind("<Control-z>", undo_text)
    tk_text.bind("<Control-y>", redo_text)
    tk_text.bind("<Control-Shift-Z>", redo_text)
    tk_text.bind("<Control-Shift-z>", redo_text)
    tk_text.bind("<KeyPress>", handle_undo_redo_shortcuts, add="+")

    screen.bind("<Control-plus>", zoom_in)
    screen.bind("<Control-equal>", zoom_in)
    screen.bind("<Control-minus>", zoom_out)
    screen.bind("<Control-b>", toolbar_controls["toggle_bold"])
    screen.bind("<Control-i>", toolbar_controls["toggle_italic"])
    screen.bind("<F5>", toolbar_controls["refresh_style_shortcut"])

    refresh_editor_ui()

    screen.mainloop()

main()
