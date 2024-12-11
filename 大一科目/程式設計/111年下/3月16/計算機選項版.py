from tkinter import *
from tkinter import ttk

def calculate():
    v1 = float(in1.get()) 
    v2 = float(in2.get())
    if combo1.current() == 0:
        lab1["text"] = str(v1 + v2)
    elif combo1.current() == 1:
        lab1["text"] = str(v1 - v2)
    elif combo1.current() == 2:
        lab1["text"] = str(v1 * v2)
    elif combo1.current() == 2:
        lab1["text"] = str(v1 / v2)

root=Tk()
root.title ('my calculator')
root.geometry ("500x100+200+100")
root.rowconfigure (0, weight=1)
root.columnconfigure (0, weight=1)
root.columnconfigure (1, weight=1)
root.columnconfigure (2, weight=1)
root.columnconfigure (3, weight=1)
root.columnconfigure (4, weight=1)
in1 = Entry (root, width=10)
in1.grid(row=0, column=0, pady=5, padx=2)

combo1 = ttk.Combobox (root, values=["+","-", "X", "/"],width=3)
combo1.current (0)
combo1.grid(row=0, column=1, pady=5, padx=2)
in2=Entry (root, width=10)
in2.grid(row=0, column=2, pady=5, padx=2)
eqBtn = Button(root, text="=",command=calculate)
eqBtn.grid (row=0, column=3)
lab1 = Label(root, text="0")
lab1.grid(row=0, column=4, padx=2, pady=5)
root.mainloop ()