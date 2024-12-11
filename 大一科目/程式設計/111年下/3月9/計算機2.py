from tkinter import *
import tkinter as tk

window = tk.Tk()
window.title('my calculator')
window.geometry('480x500')

a = 0
num = tk.StringVar()
num.set(a)

label = tk.Label(window, textvariable=num,
                borderwidth=1, relief='solid',
                background='#fff', width=30,
                font=('Arial',20), justify='left',
                anchor='e')
label.grid(row=0, column=0,columnspan=4)

# 計算函式
def test(e):
    global a
    # 如果按下等於
    if e == 'equal':
        a = eval(a)   # 使用 eval() 計算
        num.set(a)    # 設定顯示的文字變數
        a = 0         # 歸零
    # 如果按下AC
    elif e == 'empty':
        a = 0         # 歸零
        num.set(a)
    else:
        # 如果目前的數字不是 0
        if a != 0:
            a = f'{a}{e}'   # 字串相加
        else:
            a = f'{e}'      # 顯示輸入的字串
        num.set(a)


btn_7 = tk.Button(window, text='7', font=('Arial',20), width=3,height=3, command=lambda: test(7))
btn_7.grid(row=1, column=0,sticky=NSEW)
btn_8 = tk.Button(window, text='8', font=('Arial',20), width=3,height=3, command=lambda: test(8))
btn_8.grid(row=1, column=1,sticky=NSEW)
btn_9 = tk.Button(window, text='9', font=('Arial',20), width=3,height=3, command=lambda: test(9))
btn_9.grid(row=1, column=2,sticky=NSEW)
btn_a = tk.Button(window, text='+', font=('Arial',20), width=3,height=3, command=lambda: test('+'))
btn_a.grid(row=1, column=3,sticky=NSEW)

btn_4 = tk.Button(window, text='4', font=('Arial',20), width=3,height=3, command=lambda: test(4))
btn_4.grid(row=2, column=0,sticky=NSEW)
btn_5 = tk.Button(window, text='5', font=('Arial',20), width=3,height=3, command=lambda: test(5))
btn_5.grid(row=2, column=1,sticky=NSEW)
btn_6 = tk.Button(window, text='6', font=('Arial',20), width=3,height=3, command=lambda: test(6))
btn_6.grid(row=2, column=2,sticky=NSEW)
btn_b = tk.Button(window, text='-', font=('Arial',20), width=3,height=3, command=lambda: test('-'))
btn_b.grid(row=2, column=3,sticky=NSEW)

btn_3 = tk.Button(window, text='3', font=('Arial',20), width=3,height=3, command=lambda: test(3))
btn_3.grid(row=3, column=0,sticky=NSEW)
btn_2 = tk.Button(window, text='2', font=('Arial',20), width=3,height=3, command=lambda: test(2))
btn_2.grid(row=3, column=1,sticky=NSEW)
btn_1 = tk.Button(window, text='1', font=('Arial',20), width=3,height=3, command=lambda: test(1))
btn_1.grid(row=3, column=2,sticky=NSEW)
btn_c = tk.Button(window, text='x', font=('Arial',20), width=3,height=3, command=lambda: test('*'))
btn_c.grid(row=3, column=3,sticky=NSEW)

btn_ac = tk.Button(window, text='AC', font=('Arial',20), width=3,height=3, command=lambda: test('empty'))
btn_ac.grid(row=4, column=0,sticky=NSEW)
btn_0 = tk.Button(window, text='0', font=('Arial',20), width=3,height=3, command=lambda: test(0))
btn_0.grid(row=4, column=1,sticky=NSEW)
btn_e = tk.Button(window, text='=', font=('Arial',20), width=3,height=3, command=lambda: test('equal'))
btn_e.grid(row=4, column=2,sticky=NSEW)
btn_d = tk.Button(window, text='/', font=('Arial',20), width=3,height=3, command=lambda: test('/'))
btn_d.grid(row=4, column=3,sticky=NSEW)

window.mainloop()