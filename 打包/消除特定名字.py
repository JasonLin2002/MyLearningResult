import os
import tkinter as tk
from tkinter import filedialog

def create_window(main_window):
    def choose_folder():
        folder_selected = filedialog.askdirectory()
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

    def apply_removal():
        folder_path = folder_entry.get()
        remove_word = remove_word_entry.get()
        if not folder_path or not remove_word:
            result_label.config(text="請輸入資料夾路徑和要移除的字元")
            return

        for root, dirs, files in os.walk(folder_path):
            for dir_name in dirs:
                if remove_word in dir_name:
                    new_dir_name = dir_name.replace(remove_word, '')
                    os.rename(os.path.join(root, dir_name), os.path.join(root, new_dir_name))
                    result_label.config(text=f"已從資料夾名稱 '{dir_name}' 中移除特定字彙。")

            for file_name in files:
                if remove_word in file_name:
                    new_file_name = file_name.replace(remove_word, '')
                    os.rename(os.path.join(root, file_name), os.path.join(root, new_file_name))
                    result_label.config(text=f"已從檔案名稱 '{file_name}' 中移除特定字彙。")

        result_label.config(text="處理完成。")

    def back_to_main():
        window.withdraw()
        main_window.deiconify()

    window = tk.Toplevel(main_window)
    window.title("消除特定名字")

    folder_label = tk.Label(window, text="輸入資料夾位址:")
    folder_label.pack(pady=10)

    folder_entry = tk.Entry(window, width=40)
    folder_entry.pack(pady=10)

    button_choose = tk.Button(window, text="選擇資料夾", command=choose_folder)
    button_choose.pack(pady=10)

    remove_word_label = tk.Label(window, text="輸入要移除的字元:")
    remove_word_label.pack(pady=10)

    remove_word_entry = tk.Entry(window, width=40)
    remove_word_entry.pack(pady=10)

    button_apply = tk.Button(window, text="套用", command=apply_removal)
    button_apply.pack(pady=10)

    result_label = tk.Label(window, text="")
    result_label.pack(pady=10)

    back_btn = tk.Button(window, text="返回主視窗", command=back_to_main)
    back_btn.pack(pady=10)

    return window
