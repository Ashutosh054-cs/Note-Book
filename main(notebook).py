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


def get_default_font_family():
    available_fonts = {name.lower(): name for name in tkfont.families()}

    for candidate in PREFERRED_FONT_FAMILIES:
        resolved = available_fonts.get(candidate.lower())
        if resolved:
            return resolved
    return "Helvetica"


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

    editor_frame = customtkinter.CTkFrame(screen)
    editor_frame.grid(row=1, column=1, sticky="nsew", padx=(8, 10), pady=(6, 6))
    editor_frame.rowconfigure(0, weight=1)
    editor_frame.columnconfigure(0, weight=1)
    editor_frame.columnconfigure(1, weight=0)

    font_state = {"size": 18, "family": get_default_font_family()}
    current_font_size = {"value": font_state["size"]}
    #font will be replaced by the value passed on from option_font
    font = customtkinter.CTkFont(family=font_state["family"] , size=current_font_size["value"])

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

        freeze_existing_text_font(text_edit, previous_family, previous_size)

        current_font_size["value"] = clamped_size
        font_state["size"] = clamped_size
        font.configure(size=clamped_size)
        font_size_label.configure(text=f"Text Size: {clamped_size}")
        toolbar_controls["set_size"](clamped_size)

    toolbar_frame, toolbar_controls = create_formatting_toolbar(
        screen,
        text_edit,
        font_state,
        apply_font_size,
    )
    toolbar_frame.grid(row=0, column=1, sticky="ew", padx=(8, 10), pady=(10, 0))
    toolbar_controls["refresh_notebook_style"] = schedule_notebook_refresh

    def zoom_in(event=None):
        apply_font_size(current_font_size["value"] + FONT_STEP)
        schedule_notebook_refresh()
        return "break"

    def zoom_out(event=None):
        apply_font_size(current_font_size["value"] - FONT_STEP)
        schedule_notebook_refresh()
        return "break"

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
    save_btn.grid(row=0, column=0 , padx=10 , pady=(10, 6) , sticky="ew")
    open_btn.grid(row=1 , column=0 , padx=10 , pady=6 , sticky="ew")
    zoom_in_btn.grid(row=2, column=0, padx=10, pady=6, sticky="ew")
    zoom_out_btn.grid(row=3, column=0, padx=10, pady=6, sticky="ew")
    font_size_label.grid(row=4, column=0, padx=10, pady=(2, 6), sticky="w")
    #Appereance mmode change code :
    option_toggle = customtkinter.CTkOptionMenu(frame , values=["Light" , "Dark" , "System"], command=toggle_mode)
    option_toggle.grid(row=5, column=0 , padx=10, pady=(6, 10) , sticky="ew")
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

    screen.bind("<Control-plus>", zoom_in)
    screen.bind("<Control-equal>", zoom_in)
    screen.bind("<Control-minus>", zoom_out)
    screen.bind("<Control-b>", toolbar_controls["toggle_bold"])
    screen.bind("<Control-i>", toolbar_controls["toggle_italic"])
    screen.bind("<F5>", toolbar_controls["refresh_style_shortcut"])

    refresh_editor_ui()

    screen.mainloop()

main()
