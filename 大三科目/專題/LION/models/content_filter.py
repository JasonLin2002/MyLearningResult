# ===== models/content_filter.py =====
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple

class ContentFilter:
    """內容過濾推薦模組"""
    
    def __init__(self, products_df: pd.DataFrame):
        self.products_df = products_df
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self._build_content_model()
    
    def _build_content_model(self):
        """建立內容模型"""
        print("建立內容過濾模型...")
        
        # TF-IDF 向量化
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=None,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
        
        # 對合併文本進行向量化
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            self.products_df['combined_text']
        )
        
        print(f"TF-IDF矩陣維度: {self.tfidf_matrix.shape}")
    
    def get_content_recommendations(self, user_viewed_products: List[str], 
                                 user_price_range: Tuple[float, float] = None,
                                 top_n: int = 10) -> List[Dict]:
        """基於內容的推薦"""
        recommendations = []
        
        # 如果用戶沒有瀏覽記錄，返回熱門商品
        if not user_viewed_products:
            return self._get_popular_products(top_n)
        
        # 找到用戶瀏覽過的商品索引
        viewed_indices = []
        for product_name in user_viewed_products:
            matches = self.products_df[
                self.products_df['product_name'].str.contains(
                    product_name[:30], case=False, na=False
                )
            ]
            if not matches.empty:
                viewed_indices.append(matches.index[0])
        
        if not viewed_indices:
            return self._get_popular_products(top_n)
        
        # 計算與瀏覽商品的相似度
        similarity_scores = np.zeros(len(self.products_df))
        
        for idx in viewed_indices:
            similarities = cosine_similarity(
                self.tfidf_matrix[idx:idx+1], 
                self.tfidf_matrix
            ).flatten()
            similarity_scores += similarities
        
        # 正規化分數
        similarity_scores = similarity_scores / len(viewed_indices)
        
        # 過濾價格範圍
        filtered_df = self.products_df.copy()
        if user_price_range:
            min_price, max_price = user_price_range
            filtered_df = filtered_df[
                (filtered_df['price'] >= min_price) & 
                (filtered_df['price'] <= max_price)
            ]
        
        # 排除已瀏覽的商品
        filtered_df = filtered_df[~filtered_df.index.isin(viewed_indices)]
        
        if filtered_df.empty:
            return self._get_popular_products(top_n)
        
        # 獲取過濾後商品的相似度分數
        filtered_indices = filtered_df.index
        filtered_scores = similarity_scores[filtered_indices]
        
        # 排序並選取前N個
        top_indices = filtered_indices[np.argsort(filtered_scores)[::-1][:top_n]]
        
        for idx in top_indices:
            product = self.products_df.iloc[idx]
            recommendations.append({
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'price': product['price'],
                'activity_tags': product['activity_tags'],
                'location_tags': product['location_tags'],
                'link': product.get('link', ''),
                'score': float(similarity_scores[idx]),
                'reason': '基於您瀏覽過的相似商品',
                'method': 'content'
            })
        
        return recommendations
    
    def _get_popular_products(self, top_n: int) -> List[Dict]:
        """獲取熱門商品"""
        try:
            # 簡單以價格中等的商品作為熱門商品
            median_price = self.products_df['price'].median()
            
            # 價格過濾：選擇價格在中位數 80%-120% 範圍內的商品
            popular_df = self.products_df[
                (self.products_df['price'] >= median_price * 0.8) &
                (self.products_df['price'] <= median_price * 1.2)
            ]
            
            # 如果過濾後沒有商品，則放寬條件
            if popular_df.empty:
                popular_df = self.products_df[
                    (self.products_df['price'] >= median_price * 0.5) &
                    (self.products_df['price'] <= median_price * 2.0)
                ]
            
            # 如果還是沒有，就選擇所有商品
            if popular_df.empty:
                popular_df = self.products_df
            
            # 隨機選擇商品以增加多樣性
            if len(popular_df) > top_n:
                popular_df = popular_df.sample(n=top_n, random_state=42)
            else:
                popular_df = popular_df.head(top_n)
            
            recommendations = []
            for _, product in popular_df.iterrows():
                recommendations.append({
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'price': product['price'],
                    'activity_tags': product['activity_tags'],
                    'location_tags': product['location_tags'],
                    'link': product.get('link', ''),
                    'score': 0.5,
                    'reason': '熱門推薦商品',
                    'method': 'content'
                })
            
            return recommendations
            
        except Exception as e:
            print(f"獲取熱門商品時發生錯誤: {e}")
            # 如果出現任何錯誤，返回前N個商品
            fallback_df = self.products_df.head(top_n)
            recommendations = []
            for _, product in fallback_df.iterrows():
                recommendations.append({
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'price': product['price'],
                    'activity_tags': product['activity_tags'],
                    'location_tags': product['location_tags'],
                    'link': product.get('link', ''),
                    'score': 0.3,
                    'reason': '預設推薦商品',
                    'method': 'content'
                })
            return recommendations
    
    def get_similar_products_by_content(self, product_id: str, top_n: int = 5) -> List[Dict]:
        """根據內容獲取相似商品"""
        try:
            # 找到目標商品
            target_row = self.products_df[self.products_df['product_id'] == product_id]
            if target_row.empty:
                return []
            
            target_idx = target_row.index[0]
            
            # 計算相似度
            similarities = cosine_similarity(
                self.tfidf_matrix[target_idx:target_idx+1], 
                self.tfidf_matrix
            ).flatten()
            
            # 排除自己，獲取最相似的商品
            similarities[target_idx] = -1
            top_indices = np.argsort(similarities)[::-1][:top_n]
            
            recommendations = []
            for idx in top_indices:
                if similarities[idx] > 0:  # 只包含正相似度的商品
                    product = self.products_df.iloc[idx]
                    recommendations.append({
                        'product_id': product['product_id'],
                        'product_name': product['product_name'],
                        'price': product['price'],
                        'activity_tags': product['activity_tags'],
                        'location_tags': product['location_tags'],
                        'link': product.get('link', ''),
                        'score': float(similarities[idx]),
                        'reason': f'與商品內容相似度: {similarities[idx]:.2f}',
                        'method': 'content_similarity'
                    })
            
            return recommendations
            
        except Exception as e:
            print(f"獲取相似商品時發生錯誤: {e}")
            return []
    
    def search_products(self, query: str, top_n: int = 10) -> List[Dict]:
        """根據查詢字串搜索商品"""
        try:
            if not query.strip():
                return []
            
            # 將查詢轉換為向量
            query_vector = self.tfidf_vectorizer.transform([query.lower()])
            
            # 計算與所有商品的相似度
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # 獲取前N個最相似的商品
            top_indices = np.argsort(similarities)[::-1][:top_n]
            
            recommendations = []
            for idx in top_indices:
                if similarities[idx] > 0:  # 只包含有相關性的結果
                    product = self.products_df.iloc[idx]
                    recommendations.append({
                        'product_id': product['product_id'],
                        'product_name': product['product_name'],
                        'price': product['price'],
                        'activity_tags': product['activity_tags'],
                        'location_tags': product['location_tags'],
                        'link': product.get('link', ''),
                        'score': float(similarities[idx]),
                        'reason': f'搜索匹配度: {similarities[idx]:.2f}',
                        'method': 'search'
                    })
            
            return recommendations
            
        except Exception as e:
            print(f"搜索商品時發生錯誤: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """獲取內容過濾統計資訊"""
        try:
            stats = {
                'total_products': len(self.products_df),
                'tfidf_features': self.tfidf_matrix.shape[1] if self.tfidf_matrix is not None else 0,
                'average_content_length': self.products_df['combined_text'].str.len().mean(),
                'price_statistics': {
                    'min': float(self.products_df['price'].min()),
                    'max': float(self.products_df['price'].max()),
                    'mean': float(self.products_df['price'].mean()),
                    'median': float(self.products_df['price'].median())
                }
            }
            return stats
        except Exception as e:
            print(f"獲取統計資訊時發生錯誤: {e}")
            return {}