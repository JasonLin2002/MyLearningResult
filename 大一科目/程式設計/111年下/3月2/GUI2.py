from tkinter import *

window= Tk()
window.title('First GUI window')
window.geometry("500x400+100+50")

lab0=Label(window,bitmap='error',bg='#00ffaa',
           text='FCU, take that!',compound=LEFT)

lab1=Label(window,bg='#ccffaa',
           text='FCU, take that!',padx=5,pady=10)

lab1.pack(padx=0,pady=10)

lab0.pack()
lab1.pack()
window,mainloop()