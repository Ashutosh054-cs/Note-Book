import tkinter.font as tkfont
import customtkinter
from tkinter import TclError


def create_formatting_toolbar(parent, text_edit, font_state, on_font_family_change, on_font_size_change):
    toolbar = customtkinter.CTkFrame(parent)

    # CTkTextbox blocks the "font" option in tag_config, so formatting tags are
    # configured on the wrapped Tk Text widget directly.
    tk_text = text_edit._textbox if hasattr(text_edit, "_textbox") else text_edit

    bold_font = tkfont.Font(family=font_state["family"], size=font_state["size"], weight="bold")
    italic_font = tkfont.Font(family=font_state["family"], size=font_state["size"], slant="italic")

    def update_tag_fonts():
        bold_font.configure(family=font_state["family"], size=font_state["size"], weight="bold")
        italic_font.configure(family=font_state["family"], size=font_state["size"], slant="italic")
        tk_text.tag_config("bold", font=bold_font)
        tk_text.tag_config("italic", font=italic_font)

    def get_selection_range():
        try:
            start = tk_text.index("sel.first")
            end = tk_text.index("sel.last")
            return start, end
        except TclError:
            return None

    def toggle_tag(tag_name):
        selected = get_selection_range()
        if not selected:
            return "break"

        start, end = selected
        if tag_name in tk_text.tag_names("sel.first"):
            tk_text.tag_remove(tag_name, start, end)
        else:
            tk_text.tag_add(tag_name, start, end)
        return "break"

    def set_alignment(alignment):
        tk_text.tag_config("align_left", justify="left")
        tk_text.tag_config("align_center", justify="center")
        tk_text.tag_config("align_right", justify="right")

        start = "1.0"
        end = "end-1c"
        tk_text.tag_remove("align_left", start, end)
        tk_text.tag_remove("align_center", start, end)
        tk_text.tag_remove("align_right", start, end)
        tk_text.tag_add(alignment, start, end)

    def on_font_family_selected(choice):
        font_state["family"] = choice
        on_font_family_change(choice)
        update_tag_fonts()

    def on_font_size_selected(choice):
        size = int(choice)
        font_state["size"] = size
        on_font_size_change(size)
        update_tag_fonts()

    bold_btn = customtkinter.CTkButton(toolbar, text="Bold", width=74, command=lambda: toggle_tag("bold"))
    italic_btn = customtkinter.CTkButton(toolbar, text="Italic", width=74, command=lambda: toggle_tag("italic"))

    align_left_btn = customtkinter.CTkButton(toolbar, text="Left", width=70, command=lambda: set_alignment("align_left"))
    align_center_btn = customtkinter.CTkButton(toolbar, text="Center", width=70, command=lambda: set_alignment("align_center"))
    align_right_btn = customtkinter.CTkButton(toolbar, text="Right", width=70, command=lambda: set_alignment("align_right"))

    font_family_option = customtkinter.CTkOptionMenu(
        toolbar,
        values=["Helvetica", "Arial", "Times New Roman", "Courier New"],
        command=on_font_family_selected,
        width=170,
    )
    font_family_option.set(font_state["family"])

    size_values = [str(size) for size in range(12, 38, 2)]
    font_size_option = customtkinter.CTkOptionMenu(
        toolbar,
        values=size_values,
        command=on_font_size_selected,
        width=90,
    )
    font_size_option.set(str(font_state["size"]))

    bold_btn.grid(row=0, column=0, padx=(8, 6), pady=8)
    italic_btn.grid(row=0, column=1, padx=6, pady=8)
    align_left_btn.grid(row=0, column=2, padx=(18, 6), pady=8)
    align_center_btn.grid(row=0, column=3, padx=6, pady=8)
    align_right_btn.grid(row=0, column=4, padx=6, pady=8)
    font_family_option.grid(row=0, column=5, padx=(18, 6), pady=8)
    font_size_option.grid(row=0, column=6, padx=(6, 8), pady=8)

    toolbar.grid_columnconfigure(7, weight=1)

    update_tag_fonts()

    controls = {
        "set_size": lambda size: font_size_option.set(str(size)),
        "set_family": lambda family: font_family_option.set(family),
        "toggle_bold": lambda event=None: toggle_tag("bold"),
        "toggle_italic": lambda event=None: toggle_tag("italic"),
    }
    return toolbar, controls
