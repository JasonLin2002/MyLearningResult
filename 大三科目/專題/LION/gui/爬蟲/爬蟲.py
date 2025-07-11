import requests
from bs4 import BeautifulSoup
import time
import csv
import os
import json # 新增導入 json 模組

# 目標網址 (範例：雄獅旅遊的某個列表頁，請替換成您實際要爬的網址)
start_url = 'https://travel.liontravel.com/category/zh-tw/index' # 請根據實際需求修改

# 設定 User-Agent 模仿瀏覽器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}

# 儲存資料的列表
scraped_data = []

# 建立儲存圖片的資料夾 (如果需要下載圖片)
if not os.path.exists('lion_images'):
     os.makedirs('lion_images')

def scrape_page(url):
    """爬取單一頁面的函式"""
    try:
        print(f"正在爬取: {url}")
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status() # 檢查請求是否成功 (狀態碼 2xx)
        response.encoding = 'utf-8' # 明確指定編碼，避免亂碼
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- 提取 JSON-LD 資料 ---
        json_ld_script = soup.find('script', type='application/ld+json')
        if json_ld_script:
            try:
                # 嘗試解析 JSON 數據
                data = json.loads(json_ld_script.string)

                # JSON-LD 數據通常是一個列表，遍歷列表中的每個項目
                # 有些項目可能不是 Product 類型，需要檢查 '@type'
                for item in data:
                    if isinstance(item, dict) and item.get('@type') == 'Product':
                        title = item.get('name', 'N/A')
                        img_url = item.get('image', 'N/A')

                        # 價格和連結通常在 'offers' 內
                        offers = item.get('offers', {})
                        price = offers.get('price', 'N/A')
                        link = offers.get('url', 'N/A')

                        # 如果連結是相對路徑，轉換為絕對路徑
                        if link != 'N/A' and not link.startswith('http'):
                             link = requests.compat.urljoin(url, link)

                        # 將提取的資料加入列表
                        scraped_data.append({
                            'title': title,
                            'price': price,
                            'image_url': img_url,
                            'page_url': link
                        })

                        # (可選) 下載圖片
                        if img_url != 'N/A':
                            try:
                                img_response = requests.get(img_url, headers=headers, stream=True, timeout=10)
                                img_response.raise_for_status()
                                # 從 URL 中提取可能的檔名，如果包含查詢參數則移除
                                img_filename = img_url.split('/')[-1].split('?')[0]
                                # 確保檔名不為空
                                if not img_filename:
                                    img_filename = f"image_{len(scraped_data)}.jpg" # 提供一個預設檔名
                                img_name = os.path.join('lion_images', img_filename)
                                with open(img_name, 'wb') as f:
                                    for chunk in img_response.iter_content(1024):
                                        f.write(chunk)
                                print(f"已下載圖片: {img_name}")
                            except Exception as img_err:
                                print(f"下載圖片失敗 {img_url}: {img_err}")

            except json.JSONDecodeError as json_err:
                print(f"解析 JSON-LD 時發生錯誤: {json_err}")
            except Exception as e:
                print(f"處理 JSON-LD 資料時發生錯誤: {e}")
        else:
            print("未找到 JSON-LD script 標籤。")

        # --- 移除舊的分頁邏輯 ---
        # 因為資料是從 JSON-LD 一次性獲取，不再需要處理分頁
        print("已處理完畢 JSON-LD 資料，不進行分頁處理。")


    except requests.exceptions.Timeout:
        print(f"請求超時: {url}")
    except requests.exceptions.RequestException as e:
        print(f"請求錯誤 ({url}): {e}")
    except Exception as e:
        print(f"處理頁面時發生錯誤 ({url}): {e}")

# --- 主程式開始 ---
if __name__ == "__main__":
    scrape_page(start_url)

    # --- 儲存結果到 CSV ---
    if scraped_data:
        keys = scraped_data[0].keys()
        with open('lion_travel_data.csv', 'w', newline='', encoding='utf-8-sig') as output_file: # utf-8-sig 確保 Excel 打開正常
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(scraped_data)
        print(f"爬取完成，資料已儲存至 lion_travel_data.csv，共 {len(scraped_data)} 筆記錄。")
    else:
        print("未能爬取到任何資料。")
