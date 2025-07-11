# ===== models/tag_matcher.py =====
import pandas as pd
from typing import Dict, List, Set
import re

class TagMatcher:
    """標籤配對推薦模組"""
    
    def __init__(self, products_df: pd.DataFrame):
        self.products_df = products_df
    
    def get_tag_recommendations(self, user_tags: Dict[str, int], 
                              user_preferences: Dict = None,
                              top_n: int = 10) -> List[Dict]:
        """基於標籤權重的推薦"""
        if not user_tags:
            return []
        
        # 計算每個商品的標籤匹配分數
        product_scores = []
        
        for _, product in self.products_df.iterrows():
            score = self._calculate_tag_score(
                user_tags, 
                product['activity_tags_list'], 
                product['location_tags_list']
            )
            
            if score > 0:  # 只考慮有匹配的商品
                product_scores.append({
                    'product': product,
                    'score': score
                })
        
        # 根據用戶偏好過濾
        if user_preferences:
            product_scores = self._filter_by_preferences(product_scores, user_preferences)
        
        # 排序並選取前N個
        product_scores.sort(key=lambda x: x['score'], reverse=True)
        top_products = product_scores[:top_n]
        
        recommendations = []
        for item in top_products:
            product = item['product']
            score = item['score']
            
            # 找出匹配的標籤
            matched_tags = self._get_matched_tags(
                user_tags, 
                product['activity_tags_list'], 
                product['location_tags_list']
            )
            
            recommendations.append({
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'price': product['price'],
                'activity_tags': product['activity_tags'],
                'location_tags': product['location_tags'],
                'link': product.get('link', ''),
                'score': score,
                'reason': f"匹配您的偏好標籤: {', '.join(matched_tags)}",
                'method': 'tag_matching'
            })
        
        return recommendations
    
    def _calculate_tag_score(self, user_tags: Dict[str, int], 
                           activity_tags: List[str], 
                           location_tags: List[str]) -> float:
        """計算標籤匹配分數"""
        total_score = 0.0
        max_weight = max(user_tags.values()) if user_tags else 1
        
        # 合併商品標籤
        product_tags = set(activity_tags + location_tags)
        product_tags = {tag.lower().strip() for tag in product_tags if tag}
        
        for user_tag, weight in user_tags.items():
            user_tag_lower = user_tag.lower().strip()
            
            # 精確匹配
            if user_tag_lower in product_tags:
                total_score += weight / max_weight
                continue
            
            # 模糊匹配
            for product_tag in product_tags:
                if self._is_similar_tag(user_tag_lower, product_tag):
                    total_score += (weight / max_weight) * 0.8  # 模糊匹配權重稍低
                    break
        
        return total_score
    
    def _is_similar_tag(self, user_tag: str, product_tag: str) -> bool:
        """判斷標籤是否相似"""
        # 包含關係
        if user_tag in product_tag or product_tag in user_tag:
            return True
        
        # 特定相似性規則
        similar_pairs = [
            ('溫泉', '泡湯'), ('美食', '料理'), ('文化', '歷史'),
            ('自然', '景觀'), ('親子', '家庭'), ('主題樂園', '遊樂園'),
            ('東京', '晴空塔'), ('富士山', '富士'), ('雪', '雪景')
        ]
        
        for tag1, tag2 in similar_pairs:
            if (tag1 in user_tag and tag2 in product_tag) or \
               (tag2 in user_tag and tag1 in product_tag):
                return True
        
        return False
    
    def _get_matched_tags(self, user_tags: Dict[str, int], 
                         activity_tags: List[str], 
                         location_tags: List[str]) -> List[str]:
        """獲取匹配的標籤列表"""
        matched = []
        product_tags = set(activity_tags + location_tags)
        product_tags = {tag.lower().strip() for tag in product_tags if tag}
        
        for user_tag in user_tags.keys():
            user_tag_lower = user_tag.lower().strip()
            
            # 精確匹配
            if user_tag_lower in product_tags:
                matched.append(user_tag)
                continue
            
            # 模糊匹配
            for product_tag in product_tags:
                if self._is_similar_tag(user_tag_lower, product_tag):
                    matched.append(user_tag)
                    break
        
        return matched
    
    def _filter_by_preferences(self, product_scores: List[Dict], 
                             preferences: Dict) -> List[Dict]:
        """根據用戶偏好過濾商品"""
        filtered = []
        
        for item in product_scores:
            product = item['product']
            
            # 價格範圍過濾
            if 'price_range' in preferences:
                min_price, max_price = preferences['price_range']
                if not (min_price <= product['price'] <= max_price):
                    continue
            
            # 國內外偏好過濾
            if 'foreign_preference' in preferences:
                is_foreign = product.get('is_foreign', False)
                if preferences['foreign_preference'] != is_foreign:
                    continue
            
            filtered.append(item)
        
        return filtered