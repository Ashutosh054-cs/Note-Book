import tkinter as tk
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


def main():
    screen = tk.Tk()
    screen.title(" Note Book")
    screen.rowconfigure(0, minsize=400)
    screen.columnconfigure(1, minsize=600)
    text_edit = tk.Text(screen , font="Helvetica 18")
    text_edit.grid(row=0,column=1)

    #creating frame
    frame = tk.Frame(screen , relief=tk.RAISED, bd=2 )
    save_btn = tk.Button(frame , text="Save", command=lambda: save_file(screen ,  text_edit))
    open_btn = tk.Button(frame , text="Open folder" , command=lambda: open_file(screen , text_edit))
    save_btn.grid(row=0, column=0 , padx=5 , pady=5 , sticky="ew")
    open_btn.grid(row=1 , column=0 , padx=5 , pady=5 , sticky="ew")
    frame.grid(row=0,column=0 , sticky="ns") #ns = expand the frame to north and south

    screen.mainloop()

main()
