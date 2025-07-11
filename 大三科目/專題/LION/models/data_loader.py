# ===== models/data_loader.py =====
import pandas as pd
import json
import numpy as np
from typing import Dict, List, Any

class DataLoader:
    """資料載入和預處理模組"""
    
    def __init__(self):
        self.products_df = None
        self.users_data = None
        
    def load_products(self, file_path: str) -> pd.DataFrame:
        """載入商品資料"""
        try:
            self.products_df = pd.read_csv(file_path)
            print(f"成功載入 {len(self.products_df)} 筆商品資料")
            
            # 資料清理
            self.products_df = self._clean_products_data(self.products_df)
            return self.products_df
            
        except Exception as e:
            print(f"載入商品資料失敗: {e}")
            raise
    
    def load_users(self, file_path: str) -> Dict:
        """載入用戶資料"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 提取用戶分析資料
            self.users_data = data.get('user_analysis', {})
            print(f"成功載入 {len(self.users_data)} 位用戶資料")
            
            return self.users_data
            
        except Exception as e:
            print(f"載入用戶資料失敗: {e}")
            raise
    
    def _clean_products_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """清理商品資料"""
        # 處理缺失值
        df['product_name'] = df['product_name'].fillna('未知商品')
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
        df['activity_tags'] = df['activity_tags'].fillna('')
        df['location_tags'] = df['location_tags'].fillna('')
        df['product_detail'] = df['product_detail'].fillna('')
        
        # 處理標籤
        df['activity_tags_list'] = df['activity_tags'].apply(self._parse_tags)
        df['location_tags_list'] = df['location_tags'].apply(self._parse_tags)
        
        # 合併文本內容
        df['combined_text'] = (
            df['product_name'] + ' ' + 
            df['activity_tags'] + ' ' + 
            df['location_tags'] + ' ' + 
            df['product_detail']
        ).str.lower()
        
        return df
    
    def _parse_tags(self, tags_str: str) -> List[str]:
        """解析標籤字串"""
        if pd.isna(tags_str) or tags_str == '':
            return []
        return [tag.strip() for tag in str(tags_str).split(';') if tag.strip()]