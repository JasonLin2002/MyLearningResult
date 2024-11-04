from tkinter import *

window= Tk()
window.title('First GUI window')
window.geometry("500x400+100+50")
lab=Label(window,
          text= 'awdawd;dwawwwwdaddawbtdgddwwwwwwwwwwwwwwwwww',
          anchor='nw',
          width=30,
          height=20,
          font=('Helvetica',20,'bold','italic',UNDERLINE),
          wraplength=160,
          justify=LEFT,
          background='#ccffdd',
          foreground='#0000ff')

lab.pack()
window.mainloop()
