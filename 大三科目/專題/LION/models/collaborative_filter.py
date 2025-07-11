# ===== models/collaborative_filter.py =====
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List
from collections import defaultdict

class CollaborativeFilter:
    """協同過濾推薦模組"""
    
    def __init__(self, users_data: Dict, products_df: pd.DataFrame):
        self.users_data = users_data
        self.products_df = products_df
        self.user_similarity_matrix = None
        self.product_similarity_matrix = None
        self._build_collaborative_model()
    
    def _build_collaborative_model(self):
        """建立協同過濾模型"""
        print("建立協同過濾模型...")
        
        # 建立用戶-商品互動矩陣
        self._build_user_item_matrix()
        
        # 計算用戶相似度
        self._calculate_user_similarity()
        
    def _build_user_item_matrix(self):
        """建立用戶-商品互動矩陣"""
        # 收集所有商品名稱
        all_products = set()
        for user_data in self.users_data.values():
            products_viewed = user_data.get('products_viewed', [])
            all_products.update(products_viewed)
        
        self.all_products = list(all_products)
        self.product_to_idx = {product: idx for idx, product in enumerate(self.all_products)}
        
        # 建立用戶ID列表
        self.user_ids = list(self.users_data.keys())
        self.user_to_idx = {user: idx for idx, user in enumerate(self.user_ids)}
        
        # 初始化互動矩陣
        self.user_item_matrix = np.zeros((len(self.user_ids), len(self.all_products)))
        
        # 填充矩陣
        for user_id, user_data in self.users_data.items():
            user_idx = self.user_to_idx[user_id]
            products_viewed = user_data.get('products_viewed', [])
            
            for product in products_viewed:
                if product in self.product_to_idx:
                    product_idx = self.product_to_idx[product]
                    self.user_item_matrix[user_idx][product_idx] = 1
        
        print(f"用戶-商品矩陣維度: {self.user_item_matrix.shape}")
    
    def _calculate_user_similarity(self):
        """計算用戶相似度"""
        # 基於瀏覽記錄的相似度
        if self.user_item_matrix.shape[0] > 1:
            self.user_similarity_matrix = cosine_similarity(self.user_item_matrix)
        else:
            self.user_similarity_matrix = np.array([[1.0]])
    
    def get_collaborative_recommendations(self, target_user_id: str, 
                                        top_n: int = 10) -> List[Dict]:
        """基於協同過濾的推薦"""
        if target_user_id not in self.user_to_idx:
            return []
        
        target_user_idx = self.user_to_idx[target_user_id]
        target_user_data = self.users_data[target_user_id]
        
        # 獲取相似用戶
        similar_users = self._get_similar_users(target_user_idx, top_k=5)
        
        if not similar_users:
            return []
        
        # 收集推薦商品
        candidate_products = defaultdict(float)
        target_viewed = set(target_user_data.get('products_viewed', []))
        
        for similar_user_idx, similarity in similar_users:
            similar_user_id = self.user_ids[similar_user_idx]
            similar_user_data = self.users_data[similar_user_id]
            similar_viewed = similar_user_data.get('products_viewed', [])
            
            # 推薦相似用戶看過但目標用戶沒看過的商品
            for product in similar_viewed:
                if product not in target_viewed:
                    candidate_products[product] += similarity
        
        # 排序並選取前N個
        sorted_products = sorted(
            candidate_products.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:top_n]
        
        recommendations = []
        for product_name, score in sorted_products:
            # 在商品資料中查找匹配的商品
            matches = self.products_df[
                self.products_df['product_name'].str.contains(
                    product_name[:30], case=False, na=False
                )
            ]
            
            if not matches.empty:
                product = matches.iloc[0]
                recommendations.append({
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'price': product['price'],
                    'activity_tags': product['activity_tags'],
                    'location_tags': product['location_tags'],
                    'link': product.get('link', ''),
                    'score': float(score),
                    'reason': '與您相似的用戶也喜歡',
                    'method': 'collaborative'
                })
        
        return recommendations
    
    def _get_similar_users(self, target_user_idx: int, top_k: int = 5) -> List[tuple]:
        """獲取相似用戶"""
        if self.user_similarity_matrix is None:
            return []
        
        similarities = self.user_similarity_matrix[target_user_idx]
        
        # 排除自己
        similarities[target_user_idx] = -1
        
        # 獲取前k個相似用戶
        similar_indices = np.argsort(similarities)[::-1][:top_k]
        
        similar_users = []
        for idx in similar_indices:
            if similarities[idx] > 0:  # 只考慮正相似度
                similar_users.append((idx, similarities[idx]))
        
        return similar_users