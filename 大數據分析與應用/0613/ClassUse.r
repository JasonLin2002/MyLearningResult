# Install required packages
install.packages("tm")
install.packages("proxy")
install.packages("cluster")

# Load necessary libraries
library(tm)
library(proxy)
library(cluster)

# Sample set of documents
documents <- c(
  "The quick brown fox jumps over the lazy dog",
  "Never jump over the lazy dog quickly",
  "The quick brown fox is quick and smart",
  "Dogs are lazy and love to sleep",
  "Foxes are quick and clever animals"
)

# Create a text corpus and preprocess it
corpus <- VCorpus(VectorSource(documents))
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
corpus <- tm_map(corpus, stripWhitespace)

#================================================================================

# Create a Document-Term Matrix (DTM)
dtm <- DocumentTermMatrix(corpus)
dtm_matrix <- as.matrix(dtm)

# Compute distance matrix
dist_matrix <- dist(dtm_matrix, method = "euclidean")

print(dist_matrix)
# Output
#         1        2        3        4
# 2 2.645751
# 3 2.236068 3.464102
# 4 2.828427 2.645751 3.316625
# 5 2.828427 3.000000 2.645751 2.828427

# Apply K-Means clustering
set.seed(123)
kmeans_result <- kmeans(dtm_matrix, centers = 2)

# Print the clustering results
print(kmeans_result$cluster)
# Output
# 1 2 3 4 5 Docs
# 1 2 1 2 1 Clusters

#================================================================================

install.packages("quantmod")

library(quantmod)

getSymbols("2330.TW", src="yahoo")
# Warning message: 2330.TW contains missing values. Some functions will not work if objects contain missing values.

tsmc_data = get("2330.TW")

head(tsmc_data)
# Output

# 取得最新的報價
tail(tsmc_data)

#資料筆數
dim(tsmc_data)

#劃出報價的時間軸
chartSeries(tsmc_data)

#================================================================================

# 將資料轉換為資料框
tsmc_DF = as.data.frame(tsmc_data)

# 繪製2023年的數據圖表
chartSeries(tsmc_data, subset="2023")

# 取得最新一筆報價
latest_quote <- tail(tsmc_data, n = 1)

# 顯示最新一筆報價
print(latest_quote)

#================================================================================

chartSeries(tsmc_data, subset="2019-10::2022-12", type='line', theme= 'white')

#================================================================================

# 繪製2016年的數據圖表
chartSeries(tsmc_data["2016"])

# 繪製2016年1月的數據圖表
chartSeries(tsmc_data["2016-01"])

#================================================================================

# 繪製2016年1月至2016年3月的數據圖表
chartSeries(tsmc_data["2016-01/2016-03"])

# 繪製2016年1月1日至2016年3月15日的數據圖表
chartSeries(tsmc_data["2016-01-01/2016-03-15"])

#================================================================================

#Exercise 1
#輝達股價
getSymbols("NVDA", src="yahoo")
# Warning message: 2330.TW contains missing values. Some functions will not work if objects contain missing values.

NVDA_data = get("NVDA")

head(NVDA_data)
# Output

# 取得最新的報價
tail(NVDA_data)

#資料筆數
dim(NVDA_data)

#劃出報價的時間軸
chartSeries(NVDA_data)

chartSeries(NVDA_data, subset="2019-10::2024-6", type='line', theme= 'white')

#================================================================================

# 繪製2023年1月至2023年3月的蠟燭圖表
candleChart(tsmc_data["2023-01/2023-03"])

# 繪製2023年1月1日至2023年1月6日的蠟燭圖表
candleChart(tsmc_data["2023-01-01/2023-01-06"])

#================================================================================

if (!require(quantmod)) {
  install.packages("quantmod")
  library(quantmod)
}

library(quantmod)

# 取得台積電的股票數據
getSymbols("2330.TW", src="yahoo")
# 檢查台積電數據的結構
tsmc_data = get("2330.TW")
# 列印前五行數據
print(head(tsmc_data, 5))
# 列印最後五行數據
print(tail(tsmc_data, 5))

# 取得蘋果公司的股票數據
getSymbols("AAPL", src="yahoo")
# 檢查蘋果數據的結構
AAPL_data <- get(getSymbols("AAPL"))
# 列印前五行數據
print(head(AAPL_data, 5))
# 列印最後五行數據
print(tail(AAPL_data, 5))

# 取得工作目錄
wd <- getwd()
# 列印工作目錄
sprintf("Current working directory: %s", wd)

# 保存所有符號在當前目錄中
saveSymbols(c("AAPL", "2330.TW"), file.path = wd)

# 將AAPL和TSMC數據保存到CSV文件中
write.zoo(AAPL, "AAPL.csv", sep = ",", qmethod = "double")
write.zoo(tsmc_data, "2330.TW.csv", sep = ",", qmethod = "double")

#================================================================================ 

library(quantmod)

getSymbols("2330.TW", src="yahoo")
# Warning message: 2330.TW contains missing values. Some functions may not work properly until you replace them.

# 2330 TSMC 台積電
TSMC <- get("2330.TW")
# 移除 NA 值
TSMC <- na.omit(TSMC)

# 月數據
TSMC.m <- to.monthly(TSMC)
# 季數據
TSMC.q <- to.quarterly(TSMC)
# 年數據
TSMC.y <- to.yearly(TSMC)
# 2022 年的數據
TSMC.2022 <- TSMC["2022"]
# 2022 年的周數據
TSMC.2022w <- to.weekly(TSMC.2022)

#================================================================================

chartSeries(TSMC.2022w, grid = TRUE, up.col = "green", dn.col = "red")

#================================================================================

if (!require(quantmod)) {
  install.packages("quantmod")
  library(quantmod)
}

library(quantmod)

# 取得台積電的股票數據
getSymbols("2330.TW", src="yahoo")
# 取得TSMC數據
TSMC <- get("2330.TW")
# 移除數據中的NA值
TSMC <- na.omit(TSMC)
# 篩選2022年的數據
TSMC.2022 <- TSMC["2022"]

# 計算50日簡單移動平均線(SMA)
sma50 <- SMA(Cl(TSMC.2022), n = 50)
# 計算20日指數移動平均線(EMA)
ema20 <- EMA(Cl(TSMC.2022), n = 20)
# 計算5日加權移動平均線(WMA)
wma5 <- WMA(Cl(TSMC.2022), n = 5)

# 列印前10行TSMC 2022年的數據
print(head(TSMC.2022, 10))
# 查看SMA數據
head(sma50, 20)
# 查看WMA數據
head(wma5, 20)
