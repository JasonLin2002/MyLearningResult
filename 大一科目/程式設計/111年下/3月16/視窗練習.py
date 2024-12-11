from tkinter import *
from tkinter import messagebox

root=Tk()
root.title("GUI Demo")
root.geometry("600x500+200+100")

def openNewWindow():
    root.withdraw()
    NewWindow = Toplevel(root)
    NewWindow.title("New Window")
    NewWindow.geometry("400x300")
    Label(NewWindow,text="This is a new window").pack()
    btn = Button(NewWindow,text="Close",command=lambda:NewWindowColse(NewWindow))

def NewWindowColse(self):
    root.deiconify()
    self.destroy()

lab1 = Label(root,text="This is the main window")
lab1.pack(pady=10)
btn = Button(root,text="Click to open a new window",
             command=openNewWindow)

btn.pack(padx=10)

root.mainloop()