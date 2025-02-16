import os
from PIL import Image

def convert_webp_to_jpg(directory):
    """遍歷指定資料夾及其子資料夾，將所有 .webp 檔案轉換為 .jpg"""
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(".webp"):
                webp_path = os.path.join(foldername, filename)
                jpg_path = os.path.join(foldername, os.path.splitext(filename)[0] + ".jpg")
                
                try:
                    with Image.open(webp_path) as img:
                        img = img.convert("RGB")
                        img.save(jpg_path, "JPEG")
                    os.remove(webp_path)  # 刪除原始 WebP 檔案
                    print(f"轉換成功: {webp_path} -> {jpg_path}")
                except Exception as e:
                    print(f"轉換失敗: {webp_path}, 錯誤: {e}")

if __name__ == "__main__":
    target_directory = input("請輸入要遍歷的資料夾路徑: ").strip()
    if os.path.isdir(target_directory):
        convert_webp_to_jpg(target_directory)
        print("所有 WebP 檔案已轉換完畢。")
    else:
        print("請輸入有效的資料夾路徑！")
