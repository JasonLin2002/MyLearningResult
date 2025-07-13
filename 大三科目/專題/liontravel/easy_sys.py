#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
終端機版本混合推薦系統
基於內容過濾和協同過濾的旅遊行程推薦系統，支援直接處理雄獅旅遊JSON格式
"""

import pandas as pd
import numpy as np
import json
import os
import re
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter, defaultdict
import random
from datetime import datetime

# ====================
# 直接硬編碼資料檔案路徑
# ====================
TOUR_DATA_PATH = 'C:/Users/user/Desktop/lion/Metadata/group-20240919(1).json'  # 旅遊行程資料路徑
USER_LOGS_PATH = 'C:/Users/user/Desktop/lion/Metadata/log_202409.json'  # 用戶日誌路徑
PROCESSED_LOGS_PATH = 'processed_logs.json'  # 處理後的日誌存放路徑

class SimpleHybridRecommender:
    """簡化版混合推薦系統"""
    
    def __init__(self, tour_data_path, user_logs_path=None):
        """
        初始化推薦系統
        
        參數:
            tour_data_path: 旅遊行程資料路徑 (CSV 或 JSON)
            user_logs_path: 用戶行為日誌路徑 (JSON)
        """
        print(f"初始化混合推薦系統...")
        self.tour_data_path = tour_data_path
        self.user_logs_path = user_logs_path
        
        # 載入旅遊行程資料
        self.load_tour_data()
        
        # 預處理行程資料
        self.preprocess_tour_data()
        
        # 生成向量表示
        self.vectorize_data()
        
        # 如果有用戶日誌，載入並建立協同過濾模型
        if user_logs_path:
            self.load_user_logs()
            self.build_collaborative_models()
        else:
            self.user_profiles = {}
    
    def load_tour_data(self):
        """載入旅遊行程資料"""
        print(f"載入旅遊行程資料: {self.tour_data_path}")

        try:
            if self.tour_data_path.lower().endswith('.csv'):
                self.df = pd.read_csv(self.tour_data_path)

            elif self.tour_data_path.lower().endswith('.json'):
                with open(self.tour_data_path, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip()]
                    
                    data = []
                    for i, line in enumerate(lines):
                        try:
                            obj = json.loads(line)
                            data.append(obj)
                        except json.JSONDecodeError as e:
                            print(f"第 {i+1} 行 JSON 解析失敗: {e}")
                    
                    if not data:
                        raise ValueError("JSON Lines 檔案解析後為空，請檢查格式")

                self.df = pd.DataFrame(data)

            else:
                raise ValueError(f"不支援的檔案格式: {self.tour_data_path}")

            print(f"成功載入 {len(self.df)} 筆旅遊行程資料")

        except Exception as e:
            print(f"載入旅遊資料時發生錯誤: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)



    
    def preprocess_tour_data(self):
        """預處理旅遊行程資料"""
        print("預處理旅遊行程資料...")
        
        # 標準化欄位名稱
        column_map = {
            'TOUR_ID': 'tour_id',
            'B2C_LOW_PRICE': 'price',
            'PROD_DESC': 'description',
            'PROD_NAME': 'tour_name',
            'IMAGEURL': 'image_url',
            'PROVIDER': 'provider',
            'SHIP_PRICE': 'ship_price',
            'WEB': 'web_url'
        }
        
        # 套用欄位映射
        for old_col, new_col in column_map.items():
            if old_col in self.df.columns:
                self.df.rename(columns={old_col: new_col}, inplace=True)
        
        # 檢查是否有tour_id欄位，若無則創建
        if 'tour_id' not in self.df.columns:
            self.df['tour_id'] = [f'TOUR{i:06d}' for i in range(len(self.df))]
        
        # 處理缺失值
        for col in ['description', 'tour_name']:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna('')
        
        # 合併文本欄位
        self.df['combined_text'] = ''
        if 'tour_name' in self.df.columns:
            self.df['combined_text'] += self.df['tour_name'].fillna('')
        if 'description' in self.df.columns:
            self.df['combined_text'] += ' ' + self.df['description'].fillna('')
        
        # 處理文本
        self.df['processed_text'] = self.df['combined_text'].apply(
            lambda x: re.sub(r'[^\w\s]', '', str(x).lower())
        )
        
        # 提取標籤
        self.extract_tags()
        
        print("旅遊行程資料預處理完成")
    
    def extract_tags(self):
        """從行程內容中提取標籤"""
        print("提取行程標籤...")
        
        # 如果已有標籤欄位，直接使用
        if 'tags' in self.df.columns:
            all_tags = []
            for tags in self.df['tags'].fillna(''):
                if isinstance(tags, str):
                    tag_list = [tag.strip() for tag in tags.split(',')]
                    all_tags.extend(tag_list)
            
            self.unique_tags = list(set(tag for tag in all_tags if tag))
        else:
            # 使用TF-IDF找出最具代表性的詞作為標籤
            vectorizer = TfidfVectorizer(
                max_features=200,
                stop_words=['的', '和', '是', '在', '有', '與', '為', '了', '及', '或'],
                min_df=3,
                max_df=0.7
            )
            
            tfidf_matrix = vectorizer.fit_transform(self.df['processed_text'])
            feature_names = vectorizer.get_feature_names_out()
            
            # 為每個行程選取最重要的詞作為標籤
            self.df['tags'] = ''
            for i, doc in enumerate(tfidf_matrix):
                top_indices = doc.toarray()[0].argsort()[-5:][::-1]
                top_tags = [feature_names[idx] for idx in top_indices if doc[0, idx] > 0]
                self.df.at[i, 'tags'] = ','.join(top_tags)
            
            self.unique_tags = feature_names.tolist()
        
        print(f"共提取 {len(self.unique_tags)} 個獨特標籤")
    
    def vectorize_data(self):
        """向量化文本資料"""
        print("向量化文本資料...")
        
        # 使用TF-IDF向量化
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['processed_text'])
        
        print(f"向量化完成，向量維度: {self.tfidf_matrix.shape}")
    
    def load_user_logs(self):
        """載入用戶行為日誌"""
        if not self.user_logs_path or not os.path.exists(self.user_logs_path):
            print(f"警告: 找不到用戶日誌 {self.user_logs_path}")
            self.user_profiles = {}
            return
        
        print(f"載入用戶行為日誌: {self.user_logs_path}")
        
        try:
            # 讀取並解析JSON
            with open(self.user_logs_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            if not isinstance(logs, list):
                logs = [logs]
            
            print(f"載入 {len(logs)} 條原始日誌記錄")
            
            # 提取用戶-項目交互
            user_item_interactions = defaultdict(list)
            
            for log in logs:
                # 檢查必要欄位
                if not isinstance(log, dict) or 'luid' not in log:
                    continue
                
                user_id = log['luid']
                
                # 提取行程ID
                tour_id = None
                if 'prod_info' in log and isinstance(log['prod_info'], dict):
                    prod_info = log['prod_info']
                    if 'ProdDetail' in prod_info and isinstance(prod_info['ProdDetail'], dict):
                        tour_id = prod_info['ProdDetail'].get('TourID', None)
                
                # 只處理有行程ID的記錄
                if tour_id:
                    # 提取行為資訊
                    action_type = log.get('ptype', '')
                    timestamp = log.get('logtime', '')
                    
                    # 提取產品資訊
                    prod_name = ''
                    prod_price = 0
                    if 'prod_info' in log:
                        prod_info = log['prod_info']
                        prod_name = prod_info.get('ProdName', '')
                        prod_price = prod_info.get('ProdPrice', 0)
                    
                    # 記錄交互
                    interaction = {
                        'tour_id': tour_id,
                        'timestamp': timestamp,
                        'action': action_type,
                        'prod_name': prod_name,
                        'price': prod_price
                    }
                    
                    user_item_interactions[user_id].append(interaction)
            
            self.user_item_interactions = dict(user_item_interactions)
            print(f"成功提取 {len(self.user_item_interactions)} 位用戶的行為記錄")
            
            # 建立用戶檔案
            self.build_user_profiles()
            
        except Exception as e:
            print(f"處理用戶日誌時發生錯誤: {e}")
            import traceback
            traceback.print_exc()
            self.user_profiles = {}
    
    def build_user_profiles(self):
        """建立用戶偏好檔案"""
        print("建立用戶偏好檔案...")
        
        user_profiles = {}
        
        for user_id, interactions in self.user_item_interactions.items():
            # 提取用戶瀏覽的行程
            viewed_items = []
            item_categories = []
            price_sum = 0
            price_count = 0
            
            for interaction in interactions:
                tour_id = interaction['tour_id']
                viewed_items.append(tour_id)
                
                # 計算平均價格偏好
                if 'price' in interaction and interaction['price'] > 0:
                    price_sum += interaction['price']
                    price_count += 1
                
                # 獲取行程標籤
                tour_row = self.df[self.df['tour_id'] == tour_id]
                if not tour_row.empty and 'tags' in tour_row.columns:
                    tags = tour_row['tags'].iloc[0]
                    if isinstance(tags, str) and tags:
                        item_categories.extend(tags.split(','))
            
            # 計算標籤頻率
            category_counter = Counter(item_categories)
            top_categories = category_counter.most_common(10)
            
            # 計算平均價格偏好
            avg_price_preference = price_sum / price_count if price_count > 0 else 0
            
            # 建立用戶檔案
            user_profiles[user_id] = {
                'viewed_items': viewed_items,
                'item_count': len(set(viewed_items)),
                'top_categories': [category for category, count in top_categories],
                'category_counts': {category: count for category, count in category_counter.items()},
                'avg_price_preference': avg_price_preference
            }
        
        self.user_profiles = user_profiles
        print(f"已建立 {len(user_profiles)} 個用戶偏好檔案")
    
    def build_collaborative_models(self):
        """建立協同過濾模型"""
        # 如果用戶數量太少，則跳過
        if len(self.user_profiles) < 2:
            print("用戶數量不足，無法建立有效的協同過濾模型")
            return
        
        print("建立協同過濾模型...")
        
        # 建立用戶-項目矩陣
        user_ids = list(self.user_profiles.keys())
        item_ids = list(self.df['tour_id'])
        
        # 初始化矩陣
        user_item_matrix = np.zeros((len(user_ids), len(item_ids)))
        
        # 填充矩陣
        for i, user_id in enumerate(user_ids):
            viewed_items = self.user_profiles[user_id]['viewed_items']
            for item in viewed_items:
                if item in item_ids:
                    j = item_ids.index(item)
                    user_item_matrix[i, j] = 1
        
        # 計算項目相似度
        item_similarity = cosine_similarity(user_item_matrix.T)
        self.item_similarity_matrix = pd.DataFrame(
            item_similarity,
            index=item_ids,
            columns=item_ids
        )
        
        # 計算用戶相似度
        user_similarity = cosine_similarity(user_item_matrix)
        self.user_similarity_matrix = pd.DataFrame(
            user_similarity,
            index=user_ids,
            columns=user_ids
        )
        
        print("協同過濾模型建立完成")
    
    def content_based_recommend(self, query=None, tags=None, price_range=None, user_id=None, top_n=10):
        print("執行基於內容的推薦...")

        filtered_df = self.df.copy()

        # 自動填入使用者價格偏好
        if not price_range and user_id and user_id in self.user_profiles:
            avg_price = self.user_profiles[user_id]['avg_price_preference']
            price_range = (avg_price * 0.7, avg_price * 1.3)

        if price_range:
            min_price, max_price = price_range
            if 'price' in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df['price'] >= min_price) &
                    (filtered_df['price'] <= max_price)
                ]

        # 自動填入標籤
        if not query and not tags and user_id and user_id in self.user_profiles:
            tags = self.user_profiles[user_id]['top_categories']

        if query:
            processed_query = re.sub(r'[^\w\s]', '', query.lower())
            query_vector = self.vectorizer.transform([processed_query])
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            filtered_indices = filtered_df.index.tolist()
            similarity_scores = [(i, score) for i, score in enumerate(similarities) if i in filtered_indices]
            similarity_scores.sort(key=lambda x: x[1], reverse=True)
            top_indices = [i for i, _ in similarity_scores[:top_n]]
            recommendations = self.df.iloc[top_indices].copy()
            recommendations['score'] = [score for _, score in similarity_scores[:top_n]]
            recommendations['rec_source'] = 'content'

        elif tags:
            if 'tags' in filtered_df.columns:
                mask = filtered_df['tags'].apply(lambda x: all(tag in str(x).lower() for tag in tags))
                filtered_df = filtered_df[mask]
                if len(filtered_df) == 0:
                    mask = filtered_df['tags'].apply(lambda x: any(tag in str(x).lower() for tag in tags))
                    filtered_df = filtered_df[mask]
                recommendations = filtered_df.sample(min(top_n, len(filtered_df))).copy()
                recommendations['score'] = 1.0
                recommendations['rec_source'] = 'content'
            else:
                recommendations = filtered_df.sample(min(top_n, len(filtered_df))).copy()
                recommendations['score'] = 0.5
                recommendations['rec_source'] = 'content'
        else:
            recommendations = filtered_df.sample(min(top_n, len(filtered_df))).copy()
            recommendations['score'] = 0.5
            recommendations['rec_source'] = 'random'

        return recommendations
    
    def user_based_recommend(self, user_id, price_range=None, top_n=10):
        """基於用戶的協同過濾推薦"""
        print(f"執行基於用戶的協同過濾推薦 (用戶ID: {user_id})...")
        
        # 檢查用戶和模型是否存在
        if user_id not in self.user_profiles or not hasattr(self, 'user_similarity_matrix'):
            print(f"警告: 找不到用戶 {user_id} 或協同過濾模型未建立")
            return pd.DataFrame()
        
        # 過濾價格範圍
        filtered_df = self.df.copy()
        if price_range:
            min_price, max_price = price_range
            if 'price' in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df['price'] >= min_price) & 
                    (filtered_df['price'] <= max_price)
                ]
        
        # 獲取相似用戶
        similar_users = self.user_similarity_matrix[user_id].sort_values(ascending=False)[1:6].index.tolist()
        
        # 獲取用戶已瀏覽的行程
        user_viewed_items = set(self.user_profiles[user_id]['viewed_items'])
        
        # 從相似用戶中收集可能的推薦
        candidate_items = []
        for sim_user in similar_users:
            if sim_user in self.user_profiles:
                sim_user_items = set(self.user_profiles[sim_user]['viewed_items'])
                # 添加用戶未看過的行程
                candidate_items.extend(list(sim_user_items - user_viewed_items))
        
        if not candidate_items:
            print("找不到可推薦的行程")
            return pd.DataFrame()
        
        # 篩選符合價格範圍的行程
        candidate_df = filtered_df[filtered_df['tour_id'].isin(candidate_items)]
        
        # 計算每個行程被推薦的次數
        item_counts = Counter(candidate_items)
        
        # 排序並選擇前N個
        sorted_items = [item for item, count in item_counts.most_common(top_n)]
        
        # 構建結果
        result_items = []
        for item_id in sorted_items:
            item_df = candidate_df[candidate_df['tour_id'] == item_id]
            if not item_df.empty:
                item_row = item_df.iloc[0].to_dict()
                item_row['score'] = item_counts[item_id] / len(similar_users)
                item_row['rec_source'] = 'user'
                result_items.append(item_row)
        
        if result_items:
            return pd.DataFrame(result_items)
        else:
            return pd.DataFrame()
    
    def item_based_recommend(self, user_id=None, item_id=None, price_range=None, top_n=10):
        """基於項目的協同過濾推薦"""
        if not hasattr(self, 'item_similarity_matrix'):
            print("警告: 協同過濾模型未建立")
            return pd.DataFrame()
        
        # 需要用戶ID或項目ID
        if not user_id and not item_id:
            print("警告: 基於項目的推薦需要提供用戶ID或項目ID")
            return pd.DataFrame()
        
        # 確定源項目
        source_items = []
        
        if user_id and user_id in self.user_profiles:
            print(f"執行基於項目的協同過濾推薦 (用戶ID: {user_id})...")
            source_items = self.user_profiles[user_id]['viewed_items']
        elif item_id:
            print(f"執行基於項目的協同過濾推薦 (項目ID: {item_id})...")
            if item_id in self.item_similarity_matrix.index:
                source_items = [item_id]
            else:
                print(f"警告: 找不到項目 {item_id}")
                return pd.DataFrame()
        
        if not source_items:
            print("找不到源項目")
            return pd.DataFrame()
        
        # 過濾價格範圍
        filtered_df = self.df.copy()
        if price_range:
            min_price, max_price = price_range
            if 'price' in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df['price'] >= min_price) & 
                    (filtered_df['price'] <= max_price)
                ]
        
        # 計算相似項目
        candidate_scores = {}
        
        for source_item in source_items:
            if source_item in self.item_similarity_matrix.index:
                similar_items = self.item_similarity_matrix[source_item].sort_values(ascending=False)[1:21]
                
                for item, score in similar_items.items():
                    if item not in source_items:
                        candidate_scores[item] = candidate_scores.get(item, 0) + score
        
        if not candidate_scores:
            print("找不到相似項目")
            return pd.DataFrame()
        
        # 排序並選擇前N個
        sorted_items = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        # 構建結果
        result_items = []
        for item_id, score in sorted_items:
            item_df = filtered_df[filtered_df['tour_id'] == item_id]
            if not item_df.empty:
                item_row = item_df.iloc[0].to_dict()
                item_row['score'] = score
                item_row['rec_source'] = 'item'
                result_items.append(item_row)
        
        if result_items:
            return pd.DataFrame(result_items)
        else:
            return pd.DataFrame()
    
    def hybrid_recommend(self, user_id=None, query=None, tags=None, item_id=None, 
                         price_range=None, top_n=10):
        """混合推薦方法"""
        print("執行混合推薦...")
        
        # 權重設定
        weight_content = 0.5
        weight_user = 0.3
        weight_item = 0.2
        
        all_recommendations = []
        
        # 基於內容的推薦
        content_recs = self.content_based_recommend(
            query=query,
            tags=tags,
            price_range=price_range,
            top_n=top_n*2
        )
        
        if not content_recs.empty:
            content_recs['rec_weight'] = weight_content
            all_recommendations.append(content_recs)
        
        # 如果有用戶ID，嘗試協同過濾
        if user_id and user_id in self.user_profiles:
            # 基於用戶的協同過濾
            user_recs = self.user_based_recommend(
                user_id=user_id,
                price_range=price_range,
                top_n=top_n
            )
            
            if not user_recs.empty:
                user_recs['rec_weight'] = weight_user
                all_recommendations.append(user_recs)
            
            # 基於項目的協同過濾
            item_recs = self.item_based_recommend(
                user_id=user_id,
                price_range=price_range,
                top_n=top_n
            )
            
            if not item_recs.empty:
                item_recs['rec_weight'] = weight_item
                all_recommendations.append(item_recs)
        
        # 如果有項目ID但沒有用戶ID
        elif item_id:
            item_recs = self.item_based_recommend(
                item_id=item_id,
                price_range=price_range,
                top_n=top_n
            )
            
            if not item_recs.empty:
                item_recs['rec_weight'] = weight_item + weight_user
                all_recommendations.append(item_recs)
        
        # 如果沒有推薦結果，返回空DataFrame
        if not all_recommendations:
            print("沒有找到符合條件的推薦")
            return pd.DataFrame()
        
        # 合併所有推薦
        merged_recs = pd.concat(all_recommendations, ignore_index=True)
        
        # 整合不同來源的推薦
        scored_items = {}
        
        for _, item in merged_recs.iterrows():
            tour_id = item['tour_id']
            
            # 如果此行程已存在，更新分數
            if tour_id in scored_items:
                scored_items[tour_id]['score'] += item['rec_weight'] * item['score']
                scored_items[tour_id]['sources'].append(item['rec_source'])
            else:
                # 添加新行程
                item_dict = item.to_dict()
                item_dict['score'] = item['rec_weight'] * item['score']
                item_dict['sources'] = [item['rec_source']]
                scored_items[tour_id] = item_dict
        
        # 轉換回DataFrame
        final_recs = pd.DataFrame(list(scored_items.values()))
        
        # 如果為空，返回空DataFrame
        if final_recs.empty:
            return pd.DataFrame()
        
        # 排序並選擇前N個
        final_recs = final_recs.sort_values('score', ascending=False).head(top_n)
        
        # 合併來源
        final_recs['rec_source'] = final_recs['sources'].apply(lambda x: ', '.join(x))
        
        # 移除多餘欄位
        if 'sources' in final_recs.columns:
            final_recs = final_recs.drop('sources', axis=1)
        if 'rec_weight' in final_recs.columns:
            final_recs = final_recs.drop('rec_weight', axis=1)
        
        return final_recs.reset_index(drop=True)
    
    def get_price_range(self):
        """獲取價格範圍"""
        if 'price' in self.df.columns:
            min_price = self.df['price'].min()
            max_price = self.df['price'].max()
            return (min_price, max_price)
        return (0, 100000)
    
    def get_random_tags(self, count=5):
        """獲取隨機標籤"""
        if hasattr(self, 'unique_tags') and self.unique_tags:
            return random.sample(self.unique_tags, min(count, len(self.unique_tags)))
        return []

def load_lion_logs(logs_path, output_path=PROCESSED_LOGS_PATH):
    """載入並處理雄獅日誌格式"""
    if not os.path.exists(logs_path):
        print(f"錯誤: 找不到日誌檔案 {logs_path}")
        return None
    
    print(f"處理雄獅日誌格式: {logs_path}")
    
    try:
        # 讀取JSON
        with open(logs_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # 解析JSON
        try:
            logs = json.loads(content)
            if not isinstance(logs, list):
                logs = [logs]
            
            print(f"成功載入 {len(logs)} 條原始日誌")
            
            # 處理並保存為標準格式
            processed_logs = []
            valid_count = 0
            
            for log in logs:
                # 檢查必要欄位
                if not isinstance(log, dict) or 'luid' not in log:
                    continue
                
                user_id = log['luid']
                
                # 提取行程ID
                tour_id = None
                if 'prod_info' in log and isinstance(log['prod_info'], dict):
                    prod_info = log['prod_info']
                    if 'ProdDetail' in prod_info and isinstance(prod_info['ProdDetail'], dict):
                        tour_id = prod_info['ProdDetail'].get('TourID', None)
                
                # 只處理有行程ID的記錄
                if tour_id:
                    # 提取行為資訊
                    action_type = log.get('ptype', '')
                    timestamp = log.get('logtime', '')
                    
                    # 提取產品資訊
                    prod_name = ''
                    prod_price = 0
                    if 'prod_info' in log:
                        prod_info = log['prod_info']
                        prod_name = prod_info.get('ProdName', '')
                        prod_price = prod_info.get('ProdPrice', 0)
                    
                    # 建立標準格式日誌
                    processed_log = {
                        'luid': user_id,
                        'logtime': timestamp,
                        'ptype': action_type,
                        'type': log.get('type', 'app-rq'),
                        'prod_info': {
                            'ProdDetail': {'TourID': tour_id},
                            'ProdName': prod_name,
                            'ProdPrice': prod_price
                        }
                    }
                    
                    # 加入設備信息（如果有）
                    if 'device_info' in log and isinstance(log['device_info'], dict):
                        processed_log['device_info'] = log['device_info']
                    
                    processed_logs.append(processed_log)
                    valid_count += 1
            
            print(f"成功處理 {valid_count} 條有效日誌")
            
            # 保存處理後的日誌
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(processed_logs, f, ensure_ascii=False, indent=2)
            
            print(f"已保存處理後的日誌至 {output_path}")
            return output_path
            
        except json.JSONDecodeError as e:
            print(f"解析JSON時發生錯誤: {e}")
            return None
            
    except Exception as e:
        print(f"處理日誌時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return None

def display_recommendations(recommendations, top_n=10):
    if recommendations.empty:
        print("\n沒有找到符合條件的推薦結果。")
        return

    display_recs = recommendations.head(top_n)

    print("\n" + "=" * 80)
    print(f"推薦結果 (共 {len(display_recs)} 筆):")
    print("=" * 80)

    for i, (_, rec) in enumerate(display_recs.iterrows(), 1):
        tour_id = rec.get('tour_id', 'N/A')
        tour_name = rec.get('tour_name', 'N/A')
        price = rec.get('price', 0)
        score = rec.get('score', 0)
        source = rec.get('rec_source', 'unknown')

        description = rec.get('description', '')
        description = description[:100] + '...' if len(description) > 100 else description
        tags = rec.get('tags', '')

        print(f"{i}. [{tour_id}] {tour_name}")
        print(f"   價格: NT${price:,.0f} | 相關度: {score:.2f} | 來源: {source}")
        if 'user' in source:
            print("   🎯 根據與您行為相似的用戶推薦")
        elif 'item' in source:
            print("   🔄 根據您瀏覽過的相似行程推薦")
        elif 'content' in source:
            print("   📝 根據行程內容相似度推薦")
        if description:
            print(f"   簡介: {description}")
        if tags:
            print(f"   標籤: {tags}")
        print("-" * 80)

def create_sample_user():
    """創建範例用戶ID"""
    return str(random.randint(10000, 99999))

def interactive_mode():
    """互動模式"""
    print("\n" + "="*80)
    print("雄獅旅遊混合推薦系統 - 互動模式")
    print("="*80)
    
    # 處理雄獅日誌
    processed_logs_path = None
    if os.path.exists(USER_LOGS_PATH):
        processed_logs_path = load_lion_logs(USER_LOGS_PATH, PROCESSED_LOGS_PATH)
    
    # 初始化推薦器
    try:
        recommender = SimpleHybridRecommender(
            tour_data_path=TOUR_DATA_PATH,
            user_logs_path=processed_logs_path or PROCESSED_LOGS_PATH
        )
    except Exception as e:
        print(f"初始化推薦系統時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # 獲取或創建用戶ID
    user_id = None
    if recommender.user_profiles:
        # 從現有用戶中選擇一個
        user_id = list(recommender.user_profiles.keys())[0]
        print(f"使用現有用戶: {user_id}")
    else:
        # 創建範例用戶
        user_id = create_sample_user()
        print(f"創建範例用戶: {user_id}")
    
    while True:
        print("\n選擇操作:")
        print("1. 關鍵詞搜索")
        print("2. 標籤搜索")
        print("3. 基於用戶的推薦")
        print("4. 基於項目的推薦")
        print("5. 混合推薦")
        print("6. 系統資訊")
        print("7. 退出")
        
        choice = input("\n請輸入選項 (1-7): ")
        
        if choice == '1':
            query = input("請輸入搜索關鍵詞: ")
            price_min = input("請輸入最低價格 (按Enter使用默認值): ")
            price_max = input("請輸入最高價格 (按Enter使用默認值): ")
            
            # 處理價格範圍
            price_range = None
            if price_min or price_max:
                try:
                    min_price = float(price_min) if price_min else 0
                    max_price = float(price_max) if price_max else 1000000
                    price_range = (min_price, max_price)
                except:
                    print("警告: 無效的價格格式，使用默認範圍")
            
            recommendations = recommender.content_based_recommend(
                query=query,
                price_range=price_range,
                top_n=10
            )
            
            display_recommendations(recommendations)
            
        elif choice == '2':
            # 顯示一些隨機標籤
            random_tags = recommender.get_random_tags(10)
            print("可用標籤範例:", ", ".join(random_tags))
            
            tags_input = input("請輸入標籤 (多個標籤以逗號分隔): ")
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            
            price_range = None
            price_input = input("請輸入價格範圍 (格式: 最小值-最大值，按Enter跳過): ")
            if price_input:
                try:
                    min_price, max_price = map(float, price_input.split('-'))
                    price_range = (min_price, max_price)
                except:
                    print("警告: 無效的價格範圍格式，使用默認範圍")
            
            recommendations = recommender.content_based_recommend(
                tags=tags,
                price_range=price_range,
                top_n=10
            )
            
            display_recommendations(recommendations)
            
        elif choice == '3':
            if len(recommender.user_profiles) < 2:
                print("警告: 用戶數量不足，無法執行基於用戶的推薦")
                continue
                
            if user_id not in recommender.user_profiles:
                print(f"警告: 找不到用戶 {user_id} 的資料")
                # 嘗試使用其他用戶
                user_id = list(recommender.user_profiles.keys())[0]
                print(f"使用替代用戶: {user_id}")
            
            recommendations = recommender.user_based_recommend(
                user_id=user_id,
                top_n=10
            )
            
            display_recommendations(recommendations)
            
        elif choice == '4':
            if not hasattr(recommender, 'item_similarity_matrix'):
                print("警告: 協同過濾模型未建立，無法執行基於項目的推薦")
                continue
            
            if user_id in recommender.user_profiles:
                # 顯示用戶已瀏覽的行程
                viewed_items = recommender.user_profiles[user_id]['viewed_items']
                if viewed_items:
                    print(f"用戶已瀏覽的行程 (前5個): {', '.join(viewed_items[:5])}")
                    
                    # 自動選擇第一個行程或讓用戶選擇
                    select_item = input("請選擇行程ID作為推薦基礎 (按Enter使用第一個): ")
                    item_id = select_item if select_item else viewed_items[0]
                    
                    print(f"將為您推薦與行程 {item_id} 相似的行程")
                    
                    recommendations = recommender.item_based_recommend(
                        item_id=item_id,
                        top_n=10
                    )
                    
                    display_recommendations(recommendations)
                else:
                    print("用戶尚未瀏覽任何行程")
            else:
                print(f"找不到用戶 {user_id} 的行為記錄")
            
        elif choice == '5':
            query = input("請輸入搜索關鍵詞 (可選): ")
            
            # 處理標籤
            tags = None
            tags_input = input("請輸入標籤 (多個標籤以逗號分隔，可選): ")
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            
            # 處理價格範圍
            price_range = None
            price_input = input("請輸入價格範圍 (格式: 最小值-最大值，可選): ")
            if price_input:
                try:
                    min_price, max_price = map(float, price_input.split('-'))
                    price_range = (min_price, max_price)
                except:
                    print("警告: 無效的價格範圍格式，使用默認範圍")
            
            recommendations = recommender.hybrid_recommend(
                user_id=user_id,
                query=query if query else None,
                tags=tags,
                price_range=price_range,
                top_n=10
            )
            
            display_recommendations(recommendations)
        
        elif choice == '6':
            print("\n系統資訊:")
            print(f"旅遊行程資料: {TOUR_DATA_PATH}")
            print(f"用戶日誌: {USER_LOGS_PATH}")
            print(f"處理後的日誌: {PROCESSED_LOGS_PATH}")
            
            # 顯示資料統計
            if hasattr(recommender, 'df'):
                print(f"\n旅遊行程: {len(recommender.df)} 筆")
                print(f"標籤數量: {len(recommender.unique_tags)} 個")
                
                # 顯示價格範圍
                if 'price' in recommender.df.columns:
                    min_price = recommender.df['price'].min()
                    max_price = recommender.df['price'].max()
                    avg_price = recommender.df['price'].mean()
                    print(f"價格範圍: NT${min_price:,.0f} ~ NT${max_price:,.0f} (平均: NT${avg_price:,.0f})")
            
            # 顯示用戶統計
            if hasattr(recommender, 'user_profiles'):
                print(f"\n用戶數量: {len(recommender.user_profiles)} 位")
                
                # 當前用戶資訊
                if user_id in recommender.user_profiles:
                    profile = recommender.user_profiles[user_id]
                    viewed_count = len(set(profile.get('viewed_items', [])))
                    top_categories = profile.get('top_categories', [])[:5]
                    avg_price = profile.get('avg_price_preference', 0)
                    
                    print(f"\n當前用戶 ({user_id}) 資訊:")
                    print(f"瀏覽行程數: {viewed_count} 個")
                    if top_categories:
                        print(f"偏好標籤: {', '.join(top_categories)}")
                    if avg_price > 0:
                        print(f"平均價格偏好: NT${avg_price:,.0f}")
            
        elif choice == '7':
            print("\n感謝使用雄獅旅遊混合推薦系統！")
            break
        
        else:
            print("無效的選項，請重新選擇")

if __name__ == "__main__":
    interactive_mode()