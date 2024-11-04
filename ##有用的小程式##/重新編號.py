import os
import tkinter as tk
from tkinter import filedialog

def create_window(main_window):
    def choose_folder():
        folder_selected = filedialog.askdirectory()
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

    def apply_rename():
        folder_path = folder_entry.get()
        start_index = int(start_index_entry.get())
        rename_files_in_folder(folder_path, start_index)

    def rename_files_in_folder(folder_path, start_index):
        files = os.listdir(folder_path)
        for i, file_name in enumerate(files, start=start_index):
            _, file_extension = os.path.splitext(file_name)
            new_name = f"{i:03d}{file_extension}"
            old_path = os.path.join(folder_path, file_name)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)

    def back_to_main():
        window.withdraw()
        main_window.deiconify()

    window = tk.Toplevel(main_window)
    window.title("重新編號")

    label = tk.Label(window, text="輸入資料夾位址:")
    label.pack(pady=10)

    folder_entry = tk.Entry(window, width=40)
    folder_entry.pack(pady=10)

    label = tk.Label(window, text="重新命名編號:")
    label.pack(pady=10)

    start_index_entry = tk.Entry(window, width=10, validate="key", validatecommand=(window.register(lambda char: char.isdigit() or char == ""), "%S"))
    start_index_entry.pack(pady=10)
    start_index_entry.insert(0, "1")

    button_choose = tk.Button(window, text="選擇資料夾", command=choose_folder)
    button_choose.pack(pady=10)

    button_apply = tk.Button(window, text="套用", command=apply_rename)
    button_apply.pack(pady=10)

    back_btn = tk.Button(window, text="返回主視窗", command=back_to_main)
    back_btn.pack(pady=10)

    return window
