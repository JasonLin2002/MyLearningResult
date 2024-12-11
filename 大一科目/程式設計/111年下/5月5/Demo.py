import tkinter as tk
window = tk.Tk()
window.title("My SQL")
window.geometry('500x500')

lab1 = tk.Label(window, text="Table:",width=10)
lab2 = tk.Label(window, text="欄位:",width=10)
lab3 = tk.Label(window, text="數值:",width=10)
lab4 = tk.Label(window, text="SQL:",width=10)

Enter1 = tk.Entry(window)
Enter2 = tk.Entry(window)
Enter3 = tk.Entry(window)
Enter4 = tk.Entry(window)

btn1 = tk.Button(window, text="Create table", command=scrape_website,width=8)
btn2 = tk.Button(window, text="Show table", command=set_font_size,width=8)
btn3 = tk.Button(window, text="Schreach", command=open_計算機,width=8)
btn4 = tk.Button(window, text="Summit", command=open_井字,width=8)
btn5 = tk.Button(window, text="Delete table", command=change_font_color,width=8)


lab2.grid(row=0, column=0, padx=1, sticky="NSEW")   #字體大小
font_size_menu.grid(row=0, column=1, padx=1, sticky="NSEW")
btn2.grid(row=0, column=2, padx=1, sticky="NSEW")

lab4.grid(row=1, column=0, sticky="NSEW")   #字體顏色
btn5.grid(row=1, column=1, columnspan=2, sticky="NSEW")

lab3.grid(row=2, column=0, sticky="NSEW")   #額外功能
btn3.grid(row=2, column=1, sticky="NSEW")
btn4.grid(row=2, column=2, sticky="NSEW")

lab1.grid(row=3, column=0, columnspan=3, sticky="NSEW")    #爬蟲
url_entry.grid(row=4, column=0, columnspan=2, padx=1, sticky="NSEW")
btn1.grid(row=4, column=2, padx=1, sticky="NSEW")

window.mainloop()