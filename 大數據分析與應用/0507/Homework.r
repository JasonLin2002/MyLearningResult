install.packages("readr")
library(readr)

# 載入數據
bank_data <- read_delim("C:\\Users\\jk121\\Documents\\Code\\learning-result\\大數據分析與應用\\0507\\bank.csv", delim = ";")

# 檢視數據的結構
str(bank_data)

# 檢視數據的前幾行來獲取一個基本概念
head(bank_data)

#=============================================================================
# 載入所需的繪圖套件
library(ggplot2)

# 創建堆疊條形圖
ggplot(data = bank_data, aes(x = job, fill = default)) +
  geom_bar(position = "stack") +
  theme_minimal() +
  labs(title = "Job vs Default Status",
       x = "Job Type",
       y = "Count",
       fill = "Default Status")

#=============================================================================
install.packages("caTools")
install.packages("caret")
library(caTools)
library(caret)

# 設定隨機種子以確保結果的可重現性
set.seed(123)

# 準備數據，將目標變量 'y' 轉換為二元因子型變量
bank_data$y <- as.factor(ifelse(bank_data$y == "yes", 1, 0))

# 分割數據集，70% 為訓練集，30% 為測試集
split <- sample.split(bank_data$y, SplitRatio = 0.7)
train_set <- subset(bank_data, split == TRUE)
test_set <- subset(bank_data, split == FALSE)

# 使用caret包建立邏輯迴歸模型
fitControl <- trainControl(method = "cv", number = 10)
model <- train(y ~ ., data = train_set, method = "glm", family = binomial(), trControl = fitControl)

# 查看模型的詳細摘要
summary(model)

#=============================================================================
# 使用glm函數建立邏輯迴歸模型
glm_model <- glm(y ~ ., data = train_set, family = binomial())

# 計算完整模型的對數似然值
logLik_full <- logLik(glm_model)

# 建立一個空模型，僅包含截距
null_model <- glm(y ~ 1, data = train_set, family = binomial())

# 計算空模型的對數似然值
logLik_null <- logLik(null_model)

# 計算McFadden's R²
mcfadden_r2 <- 1 - (as.numeric(logLik_full) / as.numeric(logLik_null))
mcfadden_r2

#=============================================================================
# 載入所需的套件
library(car)

# 計算VIF（方差膨脹因子）
vif_values <- vif(glm_model)
vif_values

#=============================================================================
# 創建虛擬測試數據
fake_test_data <- data.frame(
  age = c(25, 45, 30),
  job = factor(c("management", "blue-collar", "technician"), levels = levels(train_set$job)),
  marital = factor(c("single", "married", "single"), levels = levels(train_set$marital)),
  education = factor(c("tertiary", "primary", "secondary"), levels = levels(train_set$education)),
  default = factor(c("no", "no", "no"), levels = levels(train_set$default)),
  balance = c(200, 1500, 0),
  housing = factor(c("yes", "no", "yes"), levels = levels(train_set$housing)),
  loan = factor(c("no", "no", "yes"), levels = levels(train_set$loan)),
  contact = factor(c("cellular", "unknown", "cellular"), levels = levels(train_set$contact)),
  day = c(15, 30, 20),
  month = factor(c("oct", "may", "apr"), levels = levels(train_set$month)),
  duration = c(300, 100, 200),
  campaign = c(1, 2, 1),
  pdays = c(-1, -1, 189),
  previous = c(0, 0, 1),
  poutcome = factor(c("unknown", "unknown", "success"), levels = levels(train_set$poutcome))
)

# 檢查是否仍有NA值
sum(is.na(fake_test_data))

# 使用更新後的模型重新進行預測
fake_test_predictions <- predict(glm_model, newdata = fake_test_data, type = "response")

# 查看預測結果
fake_test_predictions
#=============================================================================
# 使用模型對測試集進行預測，並計算預測的概率
test_predictions <- predict(glm_model, newdata = test_set, type = "response")

# 設定一個閾值來決定分類，這裡使用0.5作為常見的選擇
test_predicted_class <- ifelse(test_predictions > 0.5, 1, 0)

# 使用table函數生成混淆矩陣
confusion_matrix <- table(Predicted = test_predicted_class, Actual = test_set$y)

# 查看混淆矩陣
confusion_matrix

#=============================================================================
install.packages("pROC")

# 載入pROC包
library(pROC)

# 使用模型對測試集進行預測，計算預測概率
test_predictions <- predict(glm_model, newdata = test_set, type = "response")

# 繪製ROC曲線並計算AUC
roc_result <- roc(test_set$y, test_predictions)
plot(roc_result, main="ROC Curve")
auc(roc_result)
