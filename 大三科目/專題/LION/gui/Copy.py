import tkinter as tk
from tkinter import ttk
import json # <--- 加入這行
import os   # <--- 可能需要用來處理路徑

class MainWindow: # 或者您的主類別名稱
    def __init__(self, master):
        self.master = master
        self.products_per_page = 28
        self.current_page = 1
        self.all_products = [] # 初始化為空列表

        self.load_product_data() # 呼叫載入資料的方法
        self.setup_ui()
        self.update_display()

    def load_product_data(self):
        """從 JSON 檔案載入商品資料"""
        json_file_path = 'log_202409.json' # <--- 確認檔案名稱和路徑
        # 如果檔案不在同目錄，可能需要像這樣處理路徑:
        # script_dir = os.path.dirname(__file__)
        # json_file_path = os.path.join(script_dir, 'log_202409.json')

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                self.all_products = json.load(f)
            # 確認載入的是列表
            if not isinstance(self.all_products, list):
                print(f"錯誤：{json_file_path} 的頂層結構不是一個列表。")
                self.all_products = [] # 設回空列表避免後續錯誤
        except FileNotFoundError:
            print(f"錯誤：找不到商品資料檔案 {json_file_path}")
            self.all_products = [] # 檔案不存在，設為空列表
        except json.JSONDecodeError:
            print(f"錯誤：解析 JSON 檔案 {json_file_path} 失敗。")
            self.all_products = [] # 解析失敗，設為空列表
        except Exception as e:
            print(f"載入商品資料時發生未預期的錯誤：{e}")
            self.all_products = []

        # 更新總頁數 (如果您的分頁邏輯需要)
        self.total_products = len(self.all_products)
        self.total_pages = (self.total_products + self.products_per_page - 1) // self.products_per_page
        print(f"成功載入 {self.total_products} 件商品。總共 {self.total_pages} 頁。")

    def setup_ui(self):
        """設定 UI 介面元件"""
        # ... 您現有的 UI 設定程式碼 ...
        # 可能包含商品顯示區域的框架 (frame)
        self.product_frame = ttk.Frame(self.master)
        self.product_frame.pack(fill=tk.BOTH, expand=True)
        # 可能包含分頁按鈕等
        self.setup_pagination_controls() # 假設有此方法

    def update_display(self):
        """更新顯示在目前頁面的商品"""
        # 清除舊的商品元件 (如果有的話)
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        # 計算目前頁面要顯示的商品索引範圍
        start_index = (self.current_page - 1) * self.products_per_page
        end_index = start_index + self.products_per_page
        # 從所有商品列表中切片取得當前頁面的商品
        products_to_display = self.all_products[start_index:end_index]

        # 建立並顯示目前頁面的商品元件
        row_num, col_num = 0, 0
        for product in products_to_display:
            try:
                # *** 關鍵修改：從 product 字典中取得 ProdName ***
                product_title = product.get('ProdName', '名稱錯誤') # 使用 .get() 避免 KeyError

                # --- 這裡替換成您實際創建商品元件的程式碼 ---
                # 例如，如果原本是創建按鈕：
                button_text = f"{product_title}" # 可以加上其他資訊
                btn = ttk.Button(self.product_frame, text=button_text, command=lambda p=product: self.on_product_click(p))
                btn.grid(row=row_num, column=col_num, padx=5, pady=5, sticky="nsew")
                # --- 結束替換區 ---

                # 更新網格佈局位置
                col_num += 1
                if col_num >= 4: # 假設每行顯示 4 個商品，請根據您的佈局調整
                    col_num = 0
                    row_num += 1

            except KeyError:
                print(f"警告：商品資料缺少 'ProdName' 鍵：{product}")
                # 可以選擇跳過這個商品或顯示一個錯誤訊息
            except Exception as e:
                print(f"處理商品時發生錯誤：{product}, 錯誤：{e}")

        # 更新分頁控制項的狀態 (例如，禁用上一頁/下一頁按鈕)
        self.update_pagination_controls_state() # 假設有此方法

    def setup_pagination_controls(self):
        """設定分頁按鈕等控制項 (範例)"""
        pagination_frame = ttk.Frame(self.master)
        pagination_frame.pack(pady=10)

        self.prev_button = ttk.Button(pagination_frame, text="上一頁", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.page_label = ttk.Label(pagination_frame, text=f"頁碼: {self.current_page} / {self.total_pages}")
        self.page_label.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(pagination_frame, text="下一頁", command=self.next_page)
        self.next_button.pack(side=tk.LEFT, padx=5)

    def update_pagination_controls_state(self):
        """更新分頁按鈕的啟用/禁用狀態"""
        self.page_label.config(text=f"頁碼: {self.current_page} / {self.total_pages}")
        self.prev_button.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_page < self.total_pages else tk.DISABLED)


    def prev_page(self):
        """切換到上一頁"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_display()

    def next_page(self):
        """切換到下一頁"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_display()

    def on_product_click(self, product_data):
        """處理商品點擊事件 (範例)"""
        print(f"點擊了商品: {product_data.get('ProdName', 'N/A')}")
        # 在這裡加入您點擊商品後要執行的動作

# --- GUI 啟動程式碼 ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()