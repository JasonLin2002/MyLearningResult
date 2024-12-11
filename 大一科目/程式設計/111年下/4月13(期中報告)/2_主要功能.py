import requests
import tkinter as tk
import os
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from tkinter import colorchooser

def scrape_website():
    url = url_entry.get()
    # https://drive.google.com/drive/folders/10VqrFUfe3fHTNgeLAyDay8h0tgKXPiQ7?usp=sharing

    response = requests.get(url, cookies={'over18':'1'})
    soup = BeautifulSoup(response.text, "html.parser")
    imgs = soup.find_all('img')
    name = 0
    img_urls = []
    for i in imgs:
        img_urls.append([i['src'], name])
        name = name + 1 

    def download(url):
        print(url)
        jpg = requests.get(url[0])
        f = open(f'C:\\Users\\jk121\\Downloads\\測試圖片下載\\test_{url[1]}.jpg', 'wb')
        f.write(jpg.content)
        f.close()

    executor = ThreadPoolExecutor()
    with ThreadPoolExecutor() as executor:
        executor.map(download, img_urls)

def set_font_size():
    font_size = int(font_size_var.get())
    lab1.config(font=("Microsoft JhengHei", font_size))
    lab2.config(font=("Microsoft JhengHei", font_size))
    lab3.config(font=("Microsoft JhengHei", font_size))
    lab4.config(font=("Microsoft JhengHei", font_size))
    url_entry.config(font=("Microsoft JhengHei", font_size))
    btn1.config(font=("Microsoft JhengHei", font_size))
    btn2.config(font=("Microsoft JhengHei", font_size))
    btn3.config(font=("Microsoft JhengHei", font_size))
    btn4.config(font=("Microsoft JhengHei", font_size))
    btn5.config(font=("Microsoft JhengHei", font_size))

    font_size_menu.config(font=("Microsoft JhengHei", font_size))

def change_font_color():
    font_color = colorchooser.askcolor()[1]
    lab1.config(fg=font_color)
    lab2.config(fg=font_color)
    lab3.config(fg=font_color)
    lab4.config(fg=font_color)
    url_entry.config(fg=font_color)
    btn1.config(fg=font_color)
    btn2.config(fg=font_color)
    btn3.config(fg=font_color)
    btn4.config(fg=font_color)
    btn5.config(fg=font_color)
    font_size_menu.config(fg=font_color)
    
def open_計算機():
    os.system('3_計算機.py')

def open_井字():
    os.system('4_井字遊戲.py')

window = tk.Tk()
window.title("多功能程式")
#window.geometry('300x300')


lab1 = tk.Label(window, text="👇👇輸入網址👇👇",width=10)
lab2 = tk.Label(window, text="字體大小:",width=10)
lab3 = tk.Label(window, text="額外功能:",width=10)
lab4 = tk.Label(window, text="字體顏色:",width=10)

url_entry = tk.Entry(window)

btn1 = tk.Button(window, text="一鍵爬蟲", command=scrape_website,width=8)
btn2 = tk.Button(window, text="套用", command=set_font_size,width=8)
btn3 = tk.Button(window, text="計算機", command=open_計算機,width=8)
btn4 = tk.Button(window, text="井字遊戲", command=open_井字,width=8)
btn5 = tk.Button(window, text="調色盤選擇", command=change_font_color,width=8)



font_size_var = tk.StringVar()
font_size_var.set("10")
font_size_menu = tk.OptionMenu(window,font_size_var, *[i for i in range(10, 41, 2)])


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
