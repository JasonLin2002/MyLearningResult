from tkinter import *

window = Tk()
window.title("my calculator")
window.minsize(width=500, height=400)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)

lab1 = Label(window, text="0", justify=RIGHT, anchor=E, font="Arial 40 bold", bg="#ddddff")
lab1.grid(row=0, column=0, columnspan=4, sticky=EW, padx=0, pady=7)


number_str = "0"

flag = False
def number(n):
    global number_str
    global flag
    global flag_dot
    global flag_refresh
    if flag:
        lab1.config(text=lab1["text"]+str(n))
        number_str = number_str+str(n)
    else:
        if flag_refresh:
            number_str = "0"
            lab1.config(text=str(n), fg="black")
            flag_dot = True
        if n != 0:
            lab1.config(text=str(n))
            number_str = number_str[0:-1] + str(n)
            flag = True

flag_dot = True
def dot():
    global flag
    global flag_dot
    global number_str
    if flag_dot:
        lab1.config(text=lab1["text"]+".")
        number_str = number_str+"."
        flag = True
        flag_dot = False

flag_refresh = False
def operation(n):
    global flag
    global flag_dot
    global number_str
    global flag_refresh
    if n != "=":
        lab1.config(text="0", fg="black")
        number_str = number_str+str(n)+"0"
        flag = False
        flag_dot = True
        flag_refresh = False
    else:
        print(number_str)
        number_str = str(round(eval(number_str), 5))
        print(number_str)
        lab1.config(text=number_str, fg="blue")
        flag = False
        flag_dot = False
        flag_refresh = True

button1 = Button(window, text="1", font="Arial 30 bold", command=lambda : number(1))
button1.grid(row=1, column=0, sticky=NSEW)

button2 = Button(window, text="2", font="Arial 30 bold", command=lambda : number(2))
button2.grid(row=1, column=1, sticky=NSEW)

button3 = Button(window, text="3", font="Arial 30 bold", command=lambda : number(3))
button3.grid(row=1, column=2, sticky=NSEW)

button4 = Button(window, text="4", font="Arial 30 bold", command=lambda : number(4))
button4.grid(row=2, column=0, sticky=NSEW)

button5 = Button(window, text="5", font="Arial 30 bold", command=lambda : number(5))
button5.grid(row=2, column=1, sticky=NSEW)

button6 = Button(window, text="6", font="Arial 30 bold", command=lambda : number(6))
button6.grid(row=2, column=2, sticky=NSEW)

button7 = Button(window, text="7", font="Arial 30 bold", command=lambda : number(7))
button7.grid(row=3, column=0, sticky=NSEW)

button8 = Button(window, text="8", font="Arial 30 bold", command=lambda : number(8))
button8.grid(row=3, column=1, sticky=NSEW)

button9 = Button(window, text="9", font="Arial 30 bold", command=lambda : number(9))
button9.grid(row=3, column=2, sticky=NSEW)

button10 = Button(window, text="+", font="Arial 30 bold", command=lambda : operation("+"))
button10.grid(row=1, column=3, sticky=NSEW)

button11 = Button(window, text="-", font="Arial 30 bold", command=lambda : operation("-"))
button11.grid(row=2, column=3, sticky=NSEW)

button12 = Button(window, text="x", font="Arial 30 bold", command=lambda : operation("*"))
button12.grid(row=3, column=3, sticky=NSEW)

button13 = Button(window, text="/", font="Arial 30 bold", command=lambda : operation("/"))
button13.grid(row=4, column=3, sticky=NSEW)

button14 = Button(window, text="0", font="Arial 30 bold", command=lambda : number(0))
button14.grid(row=4, column=0, sticky=NSEW)

button15 = Button(window, text=".", font="Arial 30 bold", command=dot)
button15.grid(row=4, column=1, sticky=NSEW)

button16 = Button(window, text="=", font="Arial 30 bold", command=lambda : operation("="))
button16.grid(row=4, column=2, sticky=NSEW)

window.mainloop()
print(number_str)