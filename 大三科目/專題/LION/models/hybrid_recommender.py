# ===== models/hybrid_recommender.py =====
import pandas as pd
import json
from typing import Dict, List, Any
from .data_loader import DataLoader
from .content_filter import ContentFilter
from .collaborative_filter import CollaborativeFilter
from .tag_matcher import TagMatcher

class HybridRecommender:
    """混合推薦系統主類"""
    
    def __init__(self, products_path: str, users_path: str):
        self.data_loader = DataLoader()
        
        # 載入資料
        self.products_df = self.data_loader.load_products(products_path)
        self.users_data = self.data_loader.load_users(users_path)
        
        # 初始化各推薦模組
        self.content_filter = ContentFilter(self.products_df)
        self.collaborative_filter = CollaborativeFilter(self.users_data, self.products_df)
        self.tag_matcher = TagMatcher(self.products_df)
        
        # 權重設定
        self.weights = {
            'content': 0.35,
            'collaborative': 0.30,
            'tag_matching': 0.35
        }
        
        print("混合推薦系統初始化完成！")
    
    def get_recommendations(self, user_id: str, top_n: int = 6) -> List[Dict]:
        """獲取混合推薦結果"""
        if user_id not in self.users_data:
            return self._get_default_recommendations(top_n)
        
        user_data = self.users_data[user_id]
        user_tags = user_data.get('user_tags', {})
        products_viewed = user_data.get('products_viewed', [])
        
        # 計算用戶價格偏好範圍
        avg_price = user_data.get('average_price', 0)
        price_range = None
        if avg_price > 0:
            price_range = (avg_price * 0.5, avg_price * 1.5)
        
        # 獲取各方法的推薦
        content_recs = self.content_filter.get_content_recommendations(
            products_viewed, price_range, top_n * 2
        )
        
        collaborative_recs = self.collaborative_filter.get_collaborative_recommendations(
            user_id, top_n * 2
        )
        
        user_preferences = {
            'price_range': price_range,
            'foreign_preference': user_data.get('foreign_trip_count', 0) > user_data.get('non_foreign_trip_count', 0)
        }
        
        tag_recs = self.tag_matcher.get_tag_recommendations(
            user_tags, user_preferences, top_n * 2
        )
        
        # 融合推薦結果
        final_recommendations = self._merge_recommendations(
            content_recs, collaborative_recs, tag_recs, top_n
        )
        
        return final_recommendations
    
    def _merge_recommendations(self, content_recs: List[Dict], 
                             collaborative_recs: List[Dict], 
                             tag_recs: List[Dict], 
                             top_n: int) -> List[Dict]:
        """融合多種推薦方法的結果"""
        # 收集所有推薦商品
        all_products = {}
        
        # 處理內容推薦
        for rec in content_recs:
            product_id = rec['product_id']
            if product_id not in all_products:
                all_products[product_id] = rec.copy()
                all_products[product_id]['total_score'] = 0
                all_products[product_id]['methods'] = []
            
            all_products[product_id]['total_score'] += rec['score'] * self.weights['content']
            all_products[product_id]['methods'].append('內容相似')
        
        # 處理協同過濾推薦
        for rec in collaborative_recs:
            product_id = rec['product_id']
            if product_id not in all_products:
                all_products[product_id] = rec.copy()
                all_products[product_id]['total_score'] = 0
                all_products[product_id]['methods'] = []
            
            all_products[product_id]['total_score'] += rec['score'] * self.weights['collaborative']
            all_products[product_id]['methods'].append('協同過濾')
        
        # 處理標籤推薦
        for rec in tag_recs:
            product_id = rec['product_id']
            if product_id not in all_products:
                all_products[product_id] = rec.copy()
                all_products[product_id]['total_score'] = 0
                all_products[product_id]['methods'] = []
            
            all_products[product_id]['total_score'] += rec['score'] * self.weights['tag_matching']
            all_products[product_id]['methods'].append('標籤匹配')
        
        # 排序並選取前N個
        sorted_products = sorted(
            all_products.values(),
            key=lambda x: x['total_score'],
            reverse=True
        )[:top_n]
        
        # 更新推薦原因
        for product in sorted_products:
            methods = list(set(product['methods']))
            product['reason'] = f"基於{', '.join(methods)}推薦"
            product['score'] = round(product['total_score'], 3)
            del product['total_score']
            del product['methods']
        
        return sorted_products
    
    def _get_default_recommendations(self, top_n: int) -> List[Dict]:
        """獲取預設推薦（新用戶）"""
        # 返回價格適中的熱門商品
        median_price = self.products_df['price'].median()
        default_products = self.products_df[
            (self.products_df['price'] >= median_price * 0.8) &
            (self.products_df['price'] <= median_price * 1.2)
        ].head(top_n)
        
        recommendations = []
        for _, product in default_products.iterrows():
            recommendations.append({
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'price': product['price'],
                'activity_tags': product['activity_tags'],
                'location_tags': product['location_tags'],
                'link': product.get('link', ''),
                'score': 0.5,
                'reason': '熱門推薦商品',
                'method': 'default'
            })
        
        return recommendations
    
    def get_user_profile(self, user_id: str) -> Dict:
        """獲取用戶檔案摘要"""
        if user_id not in self.users_data:
            return {}
        
        user_data = self.users_data[user_id]
        
        # 計算用戶偏好統計
        user_tags = user_data.get('user_tags', {})
        top_tags = sorted(user_tags.items(), key=lambda x: x[1], reverse=True)[:5]
        
        profile = {
            'user_id': user_id,
            'average_price': user_data.get('average_price', 0),
            'price_range': f"${user_data.get('lowest_price', 0):,.0f} - ${user_data.get('highest_price', 0):,.0f}",
            'foreign_trips': user_data.get('foreign_trip_count', 0),
            'domestic_trips': user_data.get('non_foreign_trip_count', 0),
            'total_viewed': len(user_data.get('products_viewed', [])),
            'top_tags': [{'tag': tag, 'weight': weight} for tag, weight in top_tags],
            'preference_type': '國外旅遊愛好者' if user_data.get('foreign_trip_count', 0) > user_data.get('non_foreign_trip_count', 0) else '國內旅遊愛好者'
        }
        
        return profile
    
    def get_recommendation_explanation(self, user_id: str, product_id: str) -> str:
        """獲取特定推薦的詳細解釋"""
        if user_id not in self.users_data:
            return "用戶資料不存在"
        
        user_data = self.users_data[user_id]
        user_tags = user_data.get('user_tags', {})
        
        # 查找商品
        product_row = self.products_df[self.products_df['product_id'] == product_id]
        if product_row.empty:
            return "商品不存在"
        
        product = product_row.iloc[0]
        explanations = []
        
        # 分析標籤匹配
        if user_tags:
            matched_tags = []
            product_tags = set()
            
            if 'activity_tags_list' in product:
                product_tags.update(product['activity_tags_list'])
            if 'location_tags_list' in product:
                product_tags.update(product['location_tags_list'])
            
            for user_tag, weight in user_tags.items():
                for product_tag in product_tags:
                    if user_tag.lower() in product_tag.lower() or product_tag.lower() in user_tag.lower():
                        matched_tags.append(f"{user_tag}(權重:{weight})")
                        break
            
            if matched_tags:
                explanations.append(f"匹配您的偏好標籤: {', '.join(matched_tags)}")
        
        # 分析價格適配
        avg_price = user_data.get('average_price', 0)
        if avg_price > 0:
            price_diff_pct = abs(product['price'] - avg_price) / avg_price * 100
            if price_diff_pct <= 30:
                explanations.append(f"價格符合您的消費習慣(平均${avg_price:,.0f})")
        
        # 分析國內外偏好
        foreign_preference = user_data.get('foreign_trip_count', 0) > user_data.get('non_foreign_trip_count', 0)
        is_foreign = product.get('is_foreign', False)
        if foreign_preference == is_foreign:
            pref_type = "國外" if foreign_preference else "國內"
            explanations.append(f"符合您的{pref_type}旅遊偏好")
        
        if explanations:
            return "; ".join(explanations)
        else:
            return "基於系統綜合分析推薦"
    
    def get_similar_products(self, product_id: str, top_n: int = 5) -> List[Dict]:
        """獲取相似商品推薦"""
        product_row = self.products_df[self.products_df['product_id'] == product_id]
        if product_row.empty:
            return []
        
        product = product_row.iloc[0]
        
        # 使用內容過濾找相似商品
        similar_products = []
        
        # 基於標籤相似度
        product_tags = set()
        if 'activity_tags_list' in product:
            product_tags.update(product['activity_tags_list'])
        if 'location_tags_list' in product:
            product_tags.update(product['location_tags_list'])
        
        for _, other_product in self.products_df.iterrows():
            if other_product['product_id'] == product_id:
                continue
            
            other_tags = set()
            if 'activity_tags_list' in other_product:
                other_tags.update(other_product['activity_tags_list'])
            if 'location_tags_list' in other_product:
                other_tags.update(other_product['location_tags_list'])
            
            # 計算標籤相似度
            if product_tags and other_tags:
                similarity = len(product_tags.intersection(other_tags)) / len(product_tags.union(other_tags))
                
                if similarity > 0:
                    similar_products.append({
                        'product_id': other_product['product_id'],
                        'product_name': other_product['product_name'],
                        'price': other_product['price'],
                        'activity_tags': other_product['activity_tags'],
                        'location_tags': other_product['location_tags'],
                        'link': other_product.get('link', ''),
                        'similarity': similarity,
                        'reason': f"與您查看的商品有{similarity:.1%}相似度"
                    })
        
        # 排序並返回前N個
        similar_products.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_products[:top_n]
    
    def get_trending_products(self, category: str = None, top_n: int = 10) -> List[Dict]:
        """獲取熱門商品推薦"""
        filtered_df = self.products_df.copy()
        
        # 按類別過濾
        if category:
            filtered_df = filtered_df[
                filtered_df['activity_tags'].str.contains(category, case=False, na=False) |
                filtered_df['location_tags'].str.contains(category, case=False, na=False)
            ]
        
        # 簡單的熱門度計算（基於價格和標籤豐富度）
        filtered_df['popularity_score'] = (
            filtered_df['activity_tags'].str.len().fillna(0) +
            filtered_df['location_tags'].str.len().fillna(0)
        ) / (filtered_df['price'] / 1000)  # 標籤豐富度 / 價格比
        
        # 排序並選取前N個
        trending_df = filtered_df.nlargest(top_n, 'popularity_score')
        
        trending_products = []
        for _, product in trending_df.iterrows():
            trending_products.append({
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'price': product['price'],
                'activity_tags': product['activity_tags'],
                'location_tags': product['location_tags'],
                'link': product.get('link', ''),
                'popularity_score': round(product['popularity_score'], 2),
                'reason': '熱門推薦'
            })
        
        return trending_products
    
    def update_user_interaction(self, user_id: str, product_id: str, interaction_type: str):
        """更新用戶互動記錄（用於線上學習）"""
        if user_id not in self.users_data:
            self.users_data[user_id] = {
                'user_tags': {},
                'products_viewed': [],
                'average_price': 0,
                'foreign_trip_count': 0,
                'non_foreign_trip_count': 0
            }
        
        # 記錄瀏覽
        if interaction_type == 'view':
            if 'products_viewed' not in self.users_data[user_id]:
                self.users_data[user_id]['products_viewed'] = []
            
            # 查找商品名稱
            product_row = self.products_df[self.products_df['product_id'] == product_id]
            if not product_row.empty:
                product_name = product_row.iloc[0]['product_name']
                if product_name not in self.users_data[user_id]['products_viewed']:
                    self.users_data[user_id]['products_viewed'].append(product_name)
                
                # 更新用戶標籤偏好
                self._update_user_tags_from_product(user_id, product_row.iloc[0])
        
        print(f"已更新用戶 {user_id} 對商品 {product_id} 的 {interaction_type} 互動")
    
    def _update_user_tags_from_product(self, user_id: str, product: pd.Series):
        """從商品更新用戶標籤偏好"""
        if 'user_tags' not in self.users_data[user_id]:
            self.users_data[user_id]['user_tags'] = {}
        
        user_tags = self.users_data[user_id]['user_tags']
        
        # 從商品標籤更新用戶偏好
        product_tags = []
        if 'activity_tags_list' in product:
            product_tags.extend(product['activity_tags_list'])
        if 'location_tags_list' in product:
            product_tags.extend(product['location_tags_list'])
        
        for tag in product_tags:
            if tag and tag.strip():
                tag = tag.strip()
                user_tags[tag] = user_tags.get(tag, 0) + 1
    
    def update_user_tag_weight(self, user_id: str, tag: str) -> bool:
        """更新用戶標籤權重（點擊標籤時調用）"""
        try:
            # 確保用戶存在
            if user_id not in self.users_data:
                # 如果用戶不存在，創建新用戶
                self.users_data[user_id] = {
                    'user_tags': {},
                    'products_viewed': [],
                    'average_price': 0,
                    'foreign_trip_count': 0,
                    'non_foreign_trip_count': 0,
                    'highest_price': 0,
                    'lowest_price': 0,
                    'purchases': [],
                    'stay_durations': {}
                }
            
            # 確保 user_tags 欄位存在
            if 'user_tags' not in self.users_data[user_id]:
                self.users_data[user_id]['user_tags'] = {}
            
            # 更新標籤權重
            current_weight = self.users_data[user_id]['user_tags'].get(tag, 0)
            self.users_data[user_id]['user_tags'][tag] = current_weight + 1
            
            print(f"用戶 {user_id} 的標籤 '{tag}' 權重更新為: {current_weight + 1}")
            
            # 可選：將更新後的資料保存到文件
            self._save_users_data()
            
            return True
            
        except Exception as e:
            print(f"更新用戶標籤權重時發生錯誤: {e}")
            return False
    
    def _save_users_data(self):
        """保存用戶資料到 JSON 文件"""
        try:
            output_data = {"user_analysis": self.users_data}
            with open('data/users.json', 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print("用戶資料已保存")
        except Exception as e:
            print(f"保存用戶資料時發生錯誤: {e}")
    
    def _personalize_search_results(self, search_results: List[Dict], user_id: str) -> List[Dict]:
        """個人化搜尋結果排序"""
        try:
            if user_id not in self.users_data:
                return search_results
            
            user_data = self.users_data[user_id]
            user_tags = user_data.get('user_tags', {})
            user_avg_price = user_data.get('average_price', 0)
            
            # 為搜尋結果添加個人化分數
            for result in search_results:
                personalized_score = result.get('score', 0)
                
                # 標籤匹配加分
                if user_tags:
                    tag_bonus = self._calculate_tag_bonus(result, user_tags)
                    personalized_score += tag_bonus * 0.3
                
                # 價格適配加分
                if user_avg_price > 0:
                    price_bonus = self._calculate_price_bonus(result.get('price', 0), user_avg_price)
                    personalized_score += price_bonus * 0.2
                
                result['personalized_score'] = personalized_score
                result['reason'] = f"搜尋結果 - 個人化評分: {personalized_score:.2f}"
            
            # 按個人化分數重新排序
            search_results.sort(key=lambda x: x.get('personalized_score', 0), reverse=True)
            
            return search_results
            
        except Exception as e:
            print(f"個人化搜尋結果時發生錯誤: {e}")
            return search_results
    
    def _calculate_tag_bonus(self, product: Dict, user_tags: Dict) -> float:
        """計算標籤匹配加分"""
        try:
            bonus = 0.0
            max_weight = max(user_tags.values()) if user_tags else 1
            
            # 獲取商品標籤
            activity_tags = product.get('activity_tags', '').split(';')
            location_tags = product.get('location_tags', '').split(';')
            all_product_tags = [tag.strip().lower() for tag in activity_tags + location_tags if tag.strip()]
            
            # 計算匹配分數
            for user_tag, weight in user_tags.items():
                user_tag_lower = user_tag.lower()
                for product_tag in all_product_tags:
                    if user_tag_lower in product_tag or product_tag in user_tag_lower:
                        bonus += (weight / max_weight) * 0.5
                        break
            
            return min(bonus, 1.0)  # 限制最大加分
            
        except Exception as e:
            print(f"計算標籤加分時發生錯誤: {e}")
            return 0.0
    
    def _calculate_price_bonus(self, product_price: float, user_avg_price: float) -> float:
        """計算價格適配加分"""
        try:
            if user_avg_price <= 0 or product_price <= 0:
                return 0.0
            
            # 計算價格差異百分比
            price_diff_pct = abs(product_price - user_avg_price) / user_avg_price
            
            # 價格越接近用戶平均消費，加分越高
            if price_diff_pct <= 0.2:  # 差異在20%內
                return 0.5
            elif price_diff_pct <= 0.4:  # 差異在40%內
                return 0.3
            elif price_diff_pct <= 0.6:  # 差異在60%內
                return 0.1
            else:
                return 0.0
            
        except Exception as e:
            print(f"計算價格加分時發生錯誤: {e}")
            return 0.0
    
    def get_statistics(self) -> Dict:
        """獲取系統統計資訊"""
        stats = {
            'total_products': len(self.products_df),
            'total_users': len(self.users_data),
            'average_product_price': self.products_df['price'].mean(),
            'price_range': {
                'min': self.products_df['price'].min(),
                'max': self.products_df['price'].max()
            },
            'top_activity_tags': [],
            'top_location_tags': [],
            'users_with_tags': 0,
            'users_with_views': 0
        }
        
        # 計算最受歡迎的標籤
        all_activity_tags = []
        all_location_tags = []
        
        for _, product in self.products_df.iterrows():
            if 'activity_tags_list' in product:
                all_activity_tags.extend(product['activity_tags_list'])
            if 'location_tags_list' in product:
                all_location_tags.extend(product['location_tags_list'])
        
        from collections import Counter
        activity_counter = Counter(all_activity_tags)
        location_counter = Counter(all_location_tags)
        
        stats['top_activity_tags'] = activity_counter.most_common(5)
        stats['top_location_tags'] = location_counter.most_common(5)
        
        # 計算用戶統計
        for user_data in self.users_data.values():
            if user_data.get('user_tags'):
                stats['users_with_tags'] += 1
            if user_data.get('products_viewed'):
                stats['users_with_views'] += 1
        
        return stats
    
    def export_user_data(self, file_path: str = None) -> str:
        """匯出用戶資料"""
        try:
            if file_path is None:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_path = f"data/users_backup_{timestamp}.json"
            
            output_data = {"user_analysis": self.users_data}
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            print(f"用戶資料已匯出至: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"匯出用戶資料時發生錯誤: {e}")
            return ""
    
    def import_user_data(self, file_path: str) -> bool:
        """匯入用戶資料"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'user_analysis' in data:
                self.users_data = data['user_analysis']
                print(f"成功匯入 {len(self.users_data)} 位用戶資料")
                return True
            else:
                print("錯誤：文件格式不正確")
                return False
                
        except Exception as e:
            print(f"匯入用戶資料時發生錯誤: {e}")
            return False
    
    def get_user_recommendations_history(self, user_id: str, days: int = 7) -> List[Dict]:
        """獲取用戶推薦歷史（模擬功能）"""
        # 這個功能需要額外的資料庫支援來儲存推薦歷史
        # 目前返回空列表，可以在未來擴展
        return []
    
    def evaluate_recommendation_quality(self, user_id: str) -> Dict:
        """評估推薦品質（模擬功能）"""
        try:
            if user_id not in self.users_data:
                return {"error": "用戶不存在"}
            
            user_data = self.users_data[user_id]
            user_tags = user_data.get('user_tags', {})
            
            # 簡單的品質評估
            quality_score = 0.0
            
            # 基於標籤數量
            if len(user_tags) >= 5:
                quality_score += 0.4
            elif len(user_tags) >= 3:
                quality_score += 0.3
            elif len(user_tags) >= 1:
                quality_score += 0.2
            
            # 基於瀏覽歷史
            viewed_count = len(user_data.get('products_viewed', []))
            if viewed_count >= 10:
                quality_score += 0.3
            elif viewed_count >= 5:
                quality_score += 0.2
            elif viewed_count >= 1:
                quality_score += 0.1
            
            # 基於價格資料完整性
            if user_data.get('average_price', 0) > 0:
                quality_score += 0.3
            
            return {
                "user_id": user_id,
                "quality_score": min(quality_score, 1.0),
                "tag_count": len(user_tags),
                "viewed_count": viewed_count,
                "has_price_data": user_data.get('average_price', 0) > 0,
                "recommendation": "很好" if quality_score >= 0.8 else "良好" if quality_score >= 0.6 else "普通" if quality_score >= 0.4 else "需要更多資料"
            }
            
        except Exception as e:
            print(f"評估推薦品質時發生錯誤: {e}")
            return {"error": str(e)}