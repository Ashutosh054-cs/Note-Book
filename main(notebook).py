import tkinter as tk
import os
import sys
from tkinter.filedialog import askopenfilename , asksaveasfilename


def save_file(screen , text_edit):
    filepath = asksaveasfilename(filetypes=[("Text Files" , "*.txt") , ("C program" , "*.c") , ("Python program" , "*.py")])

    if not filepath:
        return
    
    with open(filepath, "w") as f:
        content = text_edit.get(1.0, tk.END)
        f.write(content) 

    screen.title(f"filepath: {filepath}")


def open_file(screen , text_edit):
    filepath = askopenfilename(filetypes=[("Text Files" , "*.txt") , ("C program" , "*.c") , ("Python program" , "*.py")])

    if not filepath:
        return
    
    text_edit.delete(1.0,tk.END)
    with open(filepath, "r") as f:
        content = f.read()
        text_edit.insert(tk.END, content)

    screen.title(f"filepath: {filepath}")


def update_status_bar(text_edit , status_bar):
    line , col = text_edit.index(tk.INSERT).split(".")
    content = text_edit.get("1.0" , "end-1c")
    chars = len(content)
    words = len(content.split())
    status_bar.config(text=f"Line: {int(line)}   Col: {int(col) + 1}   Chars: {chars}   Words: {words}")


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
    screen = tk.Tk()
    screen.title(" Note Book")
    set_app_icon(screen)
    screen.rowconfigure(0, minsize=400)
    screen.rowconfigure(1, weight=0)
    screen.columnconfigure(1, minsize=600, weight=1)

    editor_frame = tk.Frame(screen)
    editor_frame.grid(row=0, column=1, sticky="nsew")
    editor_frame.rowconfigure(0, weight=1)
    editor_frame.columnconfigure(0, weight=1)

    text_edit = tk.Text(editor_frame , font="Helvetica 18" , wrap="none" , undo=True)
    text_edit.grid(row=0, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(editor_frame , orient="vertical")
    scrollbar.grid(row=0, column=1, sticky="ns")

    status_bar = tk.Label(screen , text="Line: 1   Col: 1   Chars: 0   Words: 0" ,
                          anchor="w" , relief=tk.SUNKEN)
    status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

    def refresh_editor_ui(event=None):
        update_status_bar(text_edit , status_bar)

    scrollbar.config(command=text_edit.yview)
    text_edit.config(yscrollcommand=scrollbar.set)

    #creating frame
    frame = tk.Frame(screen , relief=tk.RAISED, bd=2 )
    save_btn = tk.Button(frame , text="Save", command=lambda: save_file(screen ,  text_edit))
    open_btn = tk.Button(frame , text="Open folder" , command=lambda: open_file(screen , text_edit))
    save_btn.grid(row=0, column=0 , padx=5 , pady=5 , sticky="ew")
    open_btn.grid(row=1 , column=0 , padx=5 , pady=5 , sticky="ew")
    frame.grid(row=0,column=0 , sticky="ns") #ns = expand the frame to north and south

    text_edit.bind("<KeyRelease>" , refresh_editor_ui)
    text_edit.bind("<ButtonRelease-1>" , refresh_editor_ui)
    text_edit.bind("<MouseWheel>" , refresh_editor_ui)
    text_edit.bind("<Button-4>" , refresh_editor_ui)
    text_edit.bind("<Button-5>" , refresh_editor_ui)

    refresh_editor_ui()

    screen.mainloop()

main()
