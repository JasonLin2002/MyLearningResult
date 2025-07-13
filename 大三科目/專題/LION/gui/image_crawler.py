import json
import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import random
from PIL import Image
from io import BytesIO

def load_products_from_json(json_path):
    """從JSON檔案讀取商品資訊"""
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        products = []
        for item in data:
            if ('prod_info' in item and 'ProdName' in item['prod_info'] and 
                len(item['prod_info']['ProdName']) >= 15):
                products.append(item['prod_info']['ProdName'])
        return products

def extract_keywords(product_name):
    """從商品名稱提取關鍵字"""
    # 移除一些常見的無關字詞
    remove_words = ['｜', '．', '.', '【', '】', '(', ')', '（', '）', 
                   '天', '日', '自由行', '跟團', '限定', '優惠', '旅展']
    
    name = product_name
    for word in remove_words:
        name = name.replace(word, ' ')
    
    # 取前三個非空白詞彙作為關鍵字
    keywords = [word for word in name.split() if word][:3]
    return ' '.join(keywords) + ' 景點'

def download_image(keyword, save_dir):
    """搜尋並下載圖片"""
    try:
        # 建立搜尋URL並使用不同的搜尋引擎
        search_urls = [
            f"https://www.bing.com/images/search?q={urllib.parse.quote(keyword)}&first=1",
            f"https://duckduckgo.com/?q={urllib.parse.quote(keyword)}&iax=images&ia=images"
        ]
        
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
            ]),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/'
        }
        
        for search_url in search_urls:
            try:
                # 發送請求
                response = requests.get(search_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 找到圖片URL
                    img_elements = soup.find_all('img')
                    for img in img_elements[1:6]:  # 跳過第一個，嘗試前5張圖
                        img_url = img.get('src')
                        if not img_url:
                            img_url = img.get('data-src')
                        
                        if img_url and img_url.startswith('http'):
                            try:
                                # 下載圖片
                                img_response = requests.get(img_url, headers=headers, timeout=10)
                                img = Image.open(BytesIO(img_response.content))
                                
                                # 調整圖片大小
                                target_size = (300, 200)  # 設定目標大小
                                img = img.resize(target_size, Image.Resampling.LANCZOS)
                                
                                # 儲存圖片
                                safe_filename = "".join([c for c in keyword if c.isalnum() or c in (' ', '-', '_')]).rstrip()
                                save_path = os.path.join(save_dir, f"{safe_filename}.jpg")
                                img.save(save_path, "JPEG")
                                print(f"成功下載圖片: {keyword}")
                                return True
                            except Exception as e:
                                print(f"嘗試下一張圖片: {str(e)}")
                                continue
                    
            except Exception as e:
                print(f"嘗試下一個搜尋引擎: {str(e)}")
                continue
            
    except Exception as e:
        print(f"下載圖片失敗 {keyword}: {str(e)}")
    return False

def main():
    # 確保img資料夾存在
    img_dir = os.path.join(os.path.dirname(__file__), 'img')
    os.makedirs(img_dir, exist_ok=True)
    
    # 讀取JSON
    json_path = os.path.join(os.path.dirname(__file__), 'log_202409.json')
    products = load_products_from_json(json_path)
    
    print(f"找到 {len(products)} 個商品")
    
    # 下載每個商品的圖片
    for product in products:
        keyword = extract_keywords(product)
        print(f"處理商品: {keyword}")
        
        # 檢查圖片是否已經存在
        safe_filename = "".join([c for c in keyword if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        if os.path.exists(os.path.join(img_dir, f"{safe_filename}.jpg")):
            print(f"圖片已存在: {keyword}")
            continue
            
        success = download_image(keyword, img_dir)
        if success:
            # 隨機等待2-5秒，避免請求太頻繁
            time.sleep(random.uniform(2, 5))

if __name__ == "__main__":
    main()