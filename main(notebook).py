from tkinter import *

root = Tk()

#design the text editor
root.geometry("560x800")
root.title("Note Book")
root.minsize(height=560 , width=860)
root.maxsize(height=560 , width=860)


#scrollbar
scrollbar = Scrollbar(root)

#pack for scrollbar
scrollbar.pack(side=RIGHT, fill=Y)

#adding text box
text_info = Text(root , yscrollcommand=scrollbar.set)
text_info.pack(fill=BOTH)

#config scrollbar 
scrollbar.config(command=text_info.yview)

root.mainloop()

