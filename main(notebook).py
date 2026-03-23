import tkinter as tk
import customtkinter 
import os
import sys
from tkinter.filedialog import askopenfilename , asksaveasfilename

#Code for custom tkinter :
#we will use custom tkinter to toggle between dark and light mode which using the system user preference
#we will select the default mode what user had
customtkinter.set_appearance_mode("System")

MIN_FONT_SIZE = 12
MAX_FONT_SIZE = 36
FONT_STEP = 2

#function for custom tkinter mode:
def toggle_mode(new_toggle_mode):
    customtkinter.set_appearance_mode(new_toggle_mode)

def save_file(screen , text_edit):
    filepath = asksaveasfilename(filetypes=[("Text Files" , "*.txt") , ("C program" , "*.c") , ("Python program" , "*.py")
                                            , ("HTML file" , "*.html") , ("CSS file ","*.css") , ("js file", "*.js")
                                            ])

    if not filepath:
        return
    
    with open(filepath, "w", encoding="utf-8") as f:
        content = text_edit.get("1.0", "end-1c")
        f.write(content) 

    screen.title(f"filepath: {filepath}")


def open_file(screen , text_edit):
    filepath = askopenfilename(filetypes=[("Text Files" , "*.txt") , ("C program" , "*.c") , ("Python program" , "*.py")
                                            , ("HTML file" , "*.html") , ("CSS file ","*.css") , ("js file", "*.js")
                                            ])

    if not filepath:
        return
    
    text_edit.delete("1.0", tk.END)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        text_edit.insert(tk.END, content)

    screen.title(f"filepath: {filepath}")


def update_status_bar(text_edit , status_bar):
    line , col = text_edit.index(tk.INSERT).split(".")
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


def set_app_icon(screen):
    try:
        icon_path = get_asset_path("noteBook.png")
        icon_image = tk.PhotoImage(file=icon_path)
        screen.iconphoto(True, icon_image)
        screen._icon_image = icon_image
    except tk.TclError:
        pass


def main():
    screen = customtkinter.CTk()
    screen.title("Note Book")
    set_app_icon(screen)
    screen.rowconfigure(0, weight=1)
    screen.rowconfigure(1, weight=0)
    screen.columnconfigure(0, weight=0)
    screen.columnconfigure(1, weight=1)
    screen.minsize(900, 550)

    editor_frame = customtkinter.CTkFrame(screen)
    editor_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 10), pady=(10, 6))
    editor_frame.rowconfigure(0, weight=1)
    editor_frame.columnconfigure(0, weight=1)

    current_font_size = {"value": 18}
    font = customtkinter.CTkFont(family="Helvetica" , size=current_font_size["value"])

    text_edit = customtkinter.CTkTextbox(editor_frame , wrap="none" , font=font, undo=True)
    text_edit.grid(row=0, column=0, sticky="nsew")

    scrollbar = customtkinter.CTkScrollbar(editor_frame , orientation="vertical")
    scrollbar.grid(row=0, column=1, sticky="ns")

    status_bar = customtkinter.CTkLabel(screen , text="Line: 1   Col: 1   Chars: 0   Words: 0" ,
                          anchor="w")
    status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

    


    def refresh_editor_ui(event=None):
        update_status_bar(text_edit , status_bar)

    def apply_font_size(new_size):
        clamped_size = max(MIN_FONT_SIZE, min(MAX_FONT_SIZE, int(new_size)))
        current_font_size["value"] = clamped_size
        font.configure(size=clamped_size)
        font_size_label.configure(text=f"Text Size: {clamped_size}")

    def zoom_in(event=None):
        apply_font_size(current_font_size["value"] + FONT_STEP)
        return "break"

    def zoom_out(event=None):
        apply_font_size(current_font_size["value"] - FONT_STEP)
        return "break"

    scrollbar.configure(command=text_edit.yview)
    text_edit.configure(yscrollcommand=scrollbar.set)

    #creating frame
    frame = customtkinter.CTkFrame(screen)
    frame.grid_columnconfigure(0, weight=1)
    save_btn = customtkinter.CTkButton(frame , text="Save" , command=lambda: save_file(screen ,  text_edit))
    open_btn = customtkinter.CTkButton(frame , text="Open folder" , command=lambda: open_file(screen , text_edit))
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
    frame.grid(row=0,column=0 , sticky="ns", padx=(10, 6), pady=(10, 6)) #ns = expand the frame to north and south

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

    refresh_editor_ui()

    screen.mainloop()

main()
