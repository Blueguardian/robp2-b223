from tkinter import *
from tkinter import filedialog, StringVar, OptionMenu
import config

root = Tk(None, None, "Order selection")

COLOR_OPTIONS = ["black", "white", "blue"]
color_top = StringVar(root)
color_top.set(COLOR_OPTIONS[0])

ent1 = Entry(root, font=40)
ent1.grid(row=3, column=2)

def browsefunc():
    filename = filedialog.askopenfilename(filetypes=(("svg files", "*.svg"), ("All files", "*.*")))
    ent1.delete(0, END)
    ent1.insert(END, filename) # add this

def ok():
    root.destroy()



b1 = Button(root, text="Browse for file", font=40, command=browsefunc)
b1.grid(row=3, column=4)

header = Label(root)
header.grid(row=2, column=2)

color_top_drop = OptionMenu(root, color_top, *COLOR_OPTIONS)

color_top_drop.grid(row=2, column=4)

b2 = Button(root, text="Order", font=40, command=ok)
b2.grid(row=6, column=6)


root.mainloop()
