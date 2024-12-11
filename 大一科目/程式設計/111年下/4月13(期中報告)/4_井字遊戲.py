from tkinter import *
from tkinter import messagebox

flag = 0
def btnClick( btn ):
    global flag
    btn.config( text="O", state="disable") if flag == 0 else btn.config(text="x",state="disable")
    flag = (flag + 1) % 2
    
window = Tk()
window.title('Demo 02')
window.geometry("700x600+100+50")

btn00 = Button(window, width=13, height=5,
              font="Arial 20 bold",
              command=lambda:btnClick(btn00))
btn00.grid(row=0, column=0, pady=2, padx=2)

btn01 = Button(window, width=13, height=5,
               font="Arial 20 bold",
               command=lambda:btnClick(btn01))
btn01.grid(row=0, column=1, pady=2, padx=2)

btn02 = Button(window, width=13, height=5,
               font="Arial 20 bold",
               command=lambda:btnClick(btn02))
btn02.grid(row=0, column=2, pady=2, padx=2)

btn10 = Button(window, width=13, height=5,
               font="Arial 20 bold",
               command=lambda:btnClick(btn10))
btn10.grid(row=1, column=0, pady=2, padx=2)

btn11 = Button(window, width=13, height=5,
               font="Arial 20 bold",
               command=lambda:btnClick(btn11))
btn11.grid(row=1, column=1, pady=2, padx=2)

btn12 = Button(window, width=13, height=5,
               font="Arial 20 bold",
               command=lambda:btnClick(btn12))
btn12.grid(row=1, column=2, pady=2, padx=2)

btn20 = Button(window, width=13, height=5,
               font="Arial 20 bold",
               command=lambda:btnClick(btn20))
btn20.grid(row=2, column=0, pady=2, padx=2)

btn21 = Button(window, width=13, height=5,
               font="Arial 20 bold",
               command=lambda:btnClick(btn21))
btn21.grid(row=2, column=1, pady=2, padx=2)

btn22 = Button(window, width=13, height=5,
               font="Arial 20 bold",
               command=lambda:btnClick(btn22))
btn22.grid(row=2, column=2, pady=2, padx=2)
window.resizable(0, 0)
window.mainloop()