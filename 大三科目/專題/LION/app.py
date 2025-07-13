# ===== app.py =====
from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
from models.hybrid_recommender import HybridRecommender
import os

app = Flask(__name__)

# 初始化推薦系統
recommender = None

def init_recommender():
    global recommender
    try:
        print("正在初始化推薦系統...")
        recommender = HybridRecommender(
            products_path='data/products.csv',
            users_path='data/users.json'
        )
        print("推薦系統初始化完成！")
        return True
    except Exception as e:
        print(f"推薦系統初始化失敗: {e}")
        return False

@app.route('/')
def index():
    global recommender
    if recommender is None:
        if not init_recommender():
            return "推薦系統初始化失敗，請檢查資料文件", 500
    
    # 獲取用戶列表
    user_list = list(recommender.users_data.keys())[:10]  # 顯示前10個用戶
    
    # 預設用戶
    default_user = user_list[0] if user_list else None
    selected_user = request.args.get('user_id', default_user)
    
    if selected_user and selected_user in recommender.users_data:
        # 獲取推薦
        recommendations = recommender.get_recommendations(selected_user, top_n=6)
        user_profile = recommender.get_user_profile(selected_user)
    else:
        recommendations = []
        user_profile = {}
    
    return render_template('index.html', 
                         recommendations=recommendations,
                         user_list=user_list,
                         selected_user=selected_user,
                         user_profile=user_profile)

@app.route('/api/recommend/<user_id>')
def api_recommend(user_id):
    global recommender
    if recommender is None:
        return jsonify({"error": "推薦系統未初始化"}), 500
    
    try:
        recommendations = recommender.get_recommendations(user_id, top_n=6)
        return jsonify({
            "user_id": user_id,
            "recommendations": recommendations
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users')
def api_users():
    global recommender
    if recommender is None:
        return jsonify({"error": "推薦系統未初始化"}), 500
    
    users = []
    for user_id, data in recommender.users_data.items():
        users.append({
            "user_id": user_id,
            "average_price": data.get('average_price', 0),
            "foreign_trips": data.get('foreign_trip_count', 0),
            "domestic_trips": data.get('non_foreign_trip_count', 0)
        })
    
    return jsonify(users)

# 新增：處理標籤點擊的 API
@app.route('/api/update_tag', methods=['POST'])
def update_tag():
    global recommender
    if recommender is None:
        return jsonify({"error": "推薦系統未初始化"}), 500
    
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        tag = data.get('tag')
        
        if not user_id or not tag:
            return jsonify({"error": "缺少必要參數"}), 400
        
        # 更新用戶標籤權重
        success = recommender.update_user_tag_weight(user_id, tag)
        
        if success:
            # 獲取更新後的用戶檔案
            user_profile = recommender.get_user_profile(user_id)
            return jsonify({
                "success": True,
                "message": f"已將標籤 '{tag}' 權重 +1",
                "user_profile": user_profile
            })
        else:
            return jsonify({"error": "更新失敗"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 新增：獲取用戶標籤的 API
@app.route('/api/user/<user_id>/tags')
def get_user_tags(user_id):
    global recommender
    if recommender is None:
        return jsonify({"error": "推薦系統未初始化"}), 500
    
    try:
        if user_id in recommender.users_data:
            user_tags = recommender.users_data[user_id].get('user_tags', {})
            return jsonify({"user_tags": user_tags})
        else:
            return jsonify({"error": "用戶不存在"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_products():
    global recommender
    if recommender is None:
        return jsonify({"error": "推薦系統未初始化"}), 500
    
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        user_id = data.get('user_id')
        
        if not query:
            return jsonify({"error": "搜尋關鍵詞不能為空"}), 400
        
        # 使用內容過濾器進行搜索
        search_results = recommender.content_filter.search_products(query, top_n=12)
        
        # 如果有用戶ID，可以個人化排序
        if user_id and user_id in recommender.users_data:
            search_results = recommender._personalize_search_results(search_results, user_id)
        
        return jsonify({
            "success": True,
            "query": query,
            "results": search_results,
            "total": len(search_results)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# ===== 修改 models/hybrid_recommender.py - 新增方法 =====
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
    