# ===== config.py =====
import os

class Config:
    """應用配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # 資料文件路徑
    PRODUCTS_PATH = os.environ.get('PRODUCTS_PATH') or 'data/products.csv'
    USERS_PATH = os.environ.get('USERS_PATH') or 'data/users.json'
    
    # 推薦系統參數
    RECOMMENDATION_WEIGHTS = {
        'content': 0.35,
        'collaborative': 0.30,
        'tag_matching': 0.35
    }
    
    DEFAULT_RECOMMENDATIONS_COUNT = 6