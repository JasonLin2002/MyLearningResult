// 主要JavaScript功能

document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示（檢查 Bootstrap 是否存在）
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // 為推薦卡片添加點擊追蹤
    document.querySelectorAll('.recommendation-card').forEach(function(card) {
        card.addEventListener('click', function(e) {
            if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
                // 可以在這裡添加點擊追蹤邏輯
                const titleElement = this.querySelector('.card-title');
                if (titleElement) {
                    console.log('Card clicked:', titleElement.textContent);
                }
            }
        });
    });

    // 為用戶選擇下拉選單添加事件監聽器
    const userSelect = document.querySelector('select[name="user_id"]');
    if (userSelect) {
        userSelect.addEventListener('change', function() {
            handleUserChange(this);
        });
    }
});

// 重新載入推薦
function refreshRecommendations() {
    const refreshBtn = document.querySelector('button[onclick="refreshRecommendations()"]');
    
    if (refreshBtn) {
        const originalContent = refreshBtn.innerHTML;
        
        // 顯示載入狀態
        refreshBtn.innerHTML = '<div class="loading"></div> 載入中...';
        refreshBtn.disabled = true;
        
        // 延遲重新載入頁面
        setTimeout(() => {
            window.location.reload();
        }, 500);
    } else {
        // 如果找不到按鈕，直接重新載入
        window.location.reload();
    }
}

// API調用函數
async function getRecommendations(userId) {
    if (!userId) {
        console.error('User ID is required');
        return null;
    }

    try {
        const response = await fetch(`/api/recommend/${encodeURIComponent(userId)}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        return null;
    }
}

// 用戶選擇變更處理
function handleUserChange(selectElement) {
    const userId = selectElement.value;
    if (userId) {
        // 顯示載入狀態
        const loadingOption = document.createElement('option');
        loadingOption.text = '載入中...';
        loadingOption.disabled = true;
        selectElement.appendChild(loadingOption);
        selectElement.disabled = true;
        
        // 跳轉到新的用戶頁面
        window.location.href = `/?user_id=${encodeURIComponent(userId)}`;
    }
}

// 獲取用戶列表
async function getUserList() {
    try {
        const response = await fetch('/api/users');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const users = await response.json();
        return users;
    } catch (error) {
        console.error('Error fetching user list:', error);
        return [];
    }
}

// 動態載入推薦內容（AJAX方式，不重新載入整個頁面）
async function loadRecommendationsAjax(userId) {
    if (!userId) return;
    
    const recommendationsContainer = document.querySelector('.row');
    if (!recommendationsContainer) return;
    
    // 顯示載入中狀態
    recommendationsContainer.innerHTML = `
        <div class="col-12 text-center py-5">
            <div class="loading"></div>
            <p class="mt-3">正在載入推薦...</p>
        </div>
    `;
    
    try {
        const data = await getRecommendations(userId);
        
        if (data && data.recommendations && data.recommendations.length > 0) {
            renderRecommendations(data.recommendations);
        } else {
            showNoRecommendations();
        }
    } catch (error) {
        console.error('Error loading recommendations:', error);
        showErrorMessage();
    }
}

// 渲染推薦結果
function renderRecommendations(recommendations) {
    const recommendationsContainer = document.querySelector('.row');
    if (!recommendationsContainer) return;
    
    let html = '';
    
    recommendations.forEach(rec => {
        const activityTags = rec.activity_tags ? rec.activity_tags.split(';').slice(0, 3) : [];
        const locationTags = rec.location_tags ? rec.location_tags.split(';').slice(0, 3) : [];
        
        html += `
            <div class="col-lg-6 col-xl-4 mb-4">
                <div class="card recommendation-card h-100">
                    <div class="card-header d-flex justify-content-between align-items-start">
                        <div class="method-badge">
                            ${getMethodBadges(rec.method)}
                        </div>
                        <div class="score-badge">
                            <span class="badge bg-primary">${rec.score.toFixed(2)}</span>
                        </div>
                    </div>
                    
                    <div class="card-body">
                        <h5 class="card-title">${truncateText(rec.product_name, 50)}</h5>
                        
                        <div class="price-tag mb-3">
                            <i class="fas fa-tag me-1"></i>
                            <strong>NT$ ${formatPrice(rec.price)}</strong>
                        </div>

                        ${activityTags.length > 0 ? `
                        <div class="mb-2">
                            <small class="text-muted">活動標籤:</small>
                            <div class="tags-container">
                                ${activityTags.map(tag => `<span class="badge bg-light text-dark me-1">${tag.trim()}</span>`).join('')}
                            </div>
                        </div>
                        ` : ''}

                        ${locationTags.length > 0 ? `
                        <div class="mb-3">
                            <small class="text-muted">地點標籤:</small>
                            <div class="tags-container">
                                ${locationTags.map(tag => `<span class="badge bg-light text-dark me-1">${tag.trim()}</span>`).join('')}
                            </div>
                        </div>
                        ` : ''}

                        <div class="recommendation-reason">
                            <i class="fas fa-lightbulb text-warning me-1"></i>
                            <small class="text-muted">${rec.reason}</small>
                        </div>
                    </div>
                    
                    <div class="card-footer">
                        ${rec.link ? `
                        <a href="${rec.link}" target="_blank" class="btn btn-primary btn-sm w-100">
                            <i class="fas fa-external-link-alt me-1"></i>查看詳情
                        </a>
                        ` : `
                        <button class="btn btn-secondary btn-sm w-100" disabled>
                            暫無連結
                        </button>
                        `}
                    </div>
                </div>
            </div>
        `;
    });
    
    recommendationsContainer.innerHTML = html;
}

// 獲取方法標籤
function getMethodBadges(method) {
    const badges = [];
    
    if (method.includes('content')) {
        badges.push('<span class="badge bg-info">內容推薦</span>');
    }
    if (method.includes('collaborative')) {
        badges.push('<span class="badge bg-success">協同過濾</span>');
    }
    if (method.includes('tag')) {
        badges.push('<span class="badge bg-warning">標籤匹配</span>');
    }
    
    return badges.join(' ');
}

// 文字截斷
function truncateText(text, maxLength) {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

// 價格格式化
function formatPrice(price) {
    return new Intl.NumberFormat('zh-TW').format(price);
}

// 顯示無推薦結果
function showNoRecommendations() {
    const recommendationsContainer = document.querySelector('.row');
    if (!recommendationsContainer) return;
    
    recommendationsContainer.innerHTML = `
        <div class="col-12 text-center py-5">
            <i class="fas fa-search fa-3x text-muted mb-3"></i>
            <h4 class="text-muted">暫無推薦結果</h4>
            <p class="text-muted">請選擇其他用戶或稍後再試</p>
        </div>
    `;
}

// 顯示錯誤訊息
function showErrorMessage() {
    const recommendationsContainer = document.querySelector('.row');
    if (!recommendationsContainer) return;
    
    recommendationsContainer.innerHTML = `
        <div class="col-12 text-center py-5">
            <i class="fas fa-exclamation-triangle fa-3x text-danger mb-3"></i>
            <h4 class="text-danger">載入失敗</h4>
            <p class="text-muted">請檢查網路連線或稍後再試</p>
            <button class="btn btn-primary" onclick="refreshRecommendations()">重新載入</button>
        </div>
    `;
}

// 工具函數：防抖動
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 節流函數
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}