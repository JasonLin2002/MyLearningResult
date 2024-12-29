import os

def rename_files_in_directory(directory, num_chars_to_remove):
    try:
        # 確保輸入的數字有效
        if num_chars_to_remove < 0:
            print("刪除的字數必須為正數！")
            return

        # 遍歷資料夾內所有檔案
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)

            # 確保只處理檔案
            if os.path.isfile(file_path):
                # 刪除檔名的前幾個字元
                new_filename = filename[num_chars_to_remove:]

                # 確保新檔名不為空
                if new_filename:
                    new_file_path = os.path.join(directory, new_filename)
                    os.rename(file_path, new_file_path)
                    print(f"已重命名：{filename} -> {new_filename}")
                else:
                    print(f"無法重命名檔案 {filename}，新檔名為空！")

        print("檔名更新完成！")
    except Exception as e:
        print(f"執行過程中發生錯誤：{e}")

if __name__ == "__main__":
    # 輸入資料夾路徑
    directory = input("請輸入資料夾路徑：").strip()

    # 檢查資料夾是否存在
    if not os.path.isdir(directory):
        print("指定的資料夾不存在！")
    else:
        try:
            # 輸入要刪除的字元數
            num_chars_to_remove = int(input("請輸入要刪除檔名前幾個字元的數量：").strip())
            rename_files_in_directory(directory, num_chars_to_remove)
        except ValueError:
            print("請輸入有效的數字！")
