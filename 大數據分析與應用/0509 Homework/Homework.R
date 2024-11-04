# 載入數據處理套件
library(dplyr)
library(caret)

# 讀取數據
data <- read.csv("C:/Users/jk121/Documents/Code/learning-result/大數據分析與應用/0509作業/bank.csv", sep = ";")

#=============================================================================

# 檢查數據並預處理（例如轉換類別變量和處理缺失值）
data <- data %>%
  mutate_at(vars(job, marital, education, default, housing, loan, contact, poutcome, subscribed), factor)

# 將'target'變量 (subscribed) 轉換為數值型態（0和1）
data$subscribed <- ifelse(data$subscribed == "yes", 1, 0)

# 顯示處理後的數據的前幾行，以確認數據已正確轉換
print(head(data))

#=============================================================================

# 分割數據集為訓練集和測試集
set.seed(123)
trainIndex <- createDataPartition(data$subscribed, p = .8, 
                                  list = FALSE, 
                                  times = 1)
trainData <- data[trainIndex,]
testData <- data[-trainIndex,]

# 顯示訓練數據和測試數據的概要信息
print(summary(trainData))
print(summary(testData))

#=============================================================================

# 載入決策樹模型套件
library(rpart)

# 建立決策樹模型
decision_tree_model <- rpart(subscribed ~ ., data = trainData, method = "class")

# 查看決策樹模型
print(decision_tree_model)
summary(decision_tree_model)

#=============================================================================

# 載入隨機森林模型套件
library(randomForest)

# 確保目標變量為因子類型
trainData$subscribed <- as.factor(trainData$subscribed)

# 建立隨機森林模型
random_forest_model <- randomForest(subscribed ~ ., data = trainData, ntree = 100)

# 查看隨機森林模型
print(random_forest_model)
summary(random_forest_model)

#=============================================================================

# 使用隨機森林模型預測測試集
predictions <- predict(random_forest_model, newdata = testData, type = "response")

# 計算準確度
accuracy <- sum(predictions == testData$subscribed) / nrow(testData)
print(paste("Accuracy:", accuracy))

# 計算其他性能指標（例如，精確度，召回率，F1分數）
library(caret)
confusionMatrix <- confusionMatrix(as.factor(predictions), as.factor(testData$subscribed))
print(confusionMatrix)

#=============================================================================

# 獲得特徵重要性
importance <- importance(random_forest_model)
sorted_importance <- sort(importance, decreasing = TRUE)
print(sorted_importance)

# 繪製特徵重要性圖
varImpPlot(random_forest_model)

#=============================================================================

library(rpart)
library(caret)

# 建立決策樹模型
decision_tree_model <- rpart(subscribed ~ ., data = trainData, method = "class")

# 進行預測
dt_predictions <- predict(decision_tree_model, testData, type = "class")

# 計算決策樹模型的性能指標
dt_confusionMatrix <- confusionMatrix(as.factor(dt_predictions), as.factor(testData$subscribed))
print(dt_confusionMatrix)

#=============================================================================

library(randomForest)

# 假設 random_forest_model 已經建立
rf_predictions <- predict(random_forest_model, testData, type = "response")

# 計算隨機森林模型的性能指標
rf_confusionMatrix <- confusionMatrix(as.factor(rf_predictions), as.factor(testData$subscribed))
print(rf_confusionMatrix)

#=============================================================================

# 比較準確度
dt_accuracy <- dt_confusionMatrix$overall['Accuracy']
rf_accuracy <- rf_confusionMatrix$overall['Accuracy']

# 輸出比較
print(paste("Decision Tree Accuracy: ", dt_accuracy))
print(paste("Random Forest Accuracy: ", rf_accuracy))