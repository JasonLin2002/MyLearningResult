# 安裝必要的套件
install.packages("xml2")
install.packages("dplyr")
install.packages("tidyverse")
install.packages("jsonlite")
install.packages("rvest")

# 載入必要的套件
library(xml2)
library(dplyr)
library(tidyverse)
library(rvest)

# 定義 RSS feed URL（關於 Tesla Model Y 的範例 RSS feed）
rss_url <- "https://news.google.com/rss/search?q=Tesla+Model+Y&hl=en-US&gl=US&ceid=US:en"

# 讀取 RSS feed
rss_feed <- read_xml(rss_url)

# 解析 RSS feed
items <- rss_feed %>%
  xml_find_all("//item")

# 確認 items 是否成功提取
print(items[1])

#===============================================================================

# 提取連結
links <- items %>%
  xml_find_all(".//link") %>%
  xml_text()

# 確認第一個連結
print(links[1])

# 提取描述
descriptions <- items %>%
  xml_find_all(".//description") %>%
  xml_text()

# 確認第一個描述
print(descriptions[1])

# 移除 HTML 標籤的函數
remove_html_tags <- function(html_string) {
  # 解析 HTML 內容
  parsed_html <- read_html(html_string)
  # 提取文本內容
  text_content <- html_text(parsed_html)
  return(text_content)
}

# 將函數應用到所有描述中
clean_descriptions <- sapply(descriptions, remove_html_tags, USE.NAMES = FALSE)

# 確認清理後的第一個描述
print(clean_descriptions[1])

#===============================================================================

# 提取發佈日期
pub_dates <- items %>%
  xml_find_all(".//pubDate") %>%
  xml_text()

# 確認第一個發佈日期
print(pub_dates[1])

# 創建包含提取信息的資料框
# 注意：這裡缺少 title 欄位的提取，需補充
titles <- items %>%
  xml_find_all(".//title") %>%
  xml_text()

# 確認第一個標題
print(titles[1])

tesla_news <- data.frame(
  title = titles,
  link = links,
  description = clean_descriptions,
  pub_date = pub_dates,
  stringsAsFactors = FALSE
)

# 打印資料框的前幾行
print(head(tesla_news))

#===============================================================================

# 第一段程式碼
links <- items %>%
  xml_find_all(".//link") %>%
  xml_text()

# 第二段程式碼
print(links[1])

# 第三段程式碼
descriptions <- items %>%
  xml_find_all(".//description") %>%
  xml_text()

# 第四段程式碼
print(descriptions[1])

# 第五段程式碼
# 移除 HTML 標籤的函數
remove_html_tags <- function(html_string) {
  # 解析 HTML 內容
  parsed_html <- read_html(html_string)
  # 提取文本內容
  text_content <- html_text(parsed_html)
  return(text_content)
}

# 第六段程式碼
# 將函數應用到所有描述中
clean_descriptions <- sapply(descriptions, remove_html_tags, USE.NAMES = FALSE)

# 第七段程式碼
print(clean_descriptions[1])

#===============================================================================

# 第一段程式碼
pub_dates <- items %>%
  xml_find_all(".//pubDate") %>%
  xml_text()

# 第二段程式碼
print(pub_dates[1])

# 第三段程式碼
# 創建包含提取信息的資料框
tesla_news <- data.frame(
  title = titles,
  link = links,
  description = clean_descriptions,
  pub_date = pub_dates,
  stringsAsFactors = FALSE
)

# 第四段程式碼
# 打印資料框的前幾行
print(head(tesla_news))

#===============================================================================

# 第一段程式碼
# 可選：將資料框保存為 CSV 檔案
write.csv(tesla_news, "tesla_model_y_news.csv", row.names = FALSE)

#===============================================================================

# 第一段程式碼
txt <- clean_descriptions[1]

# 第二段程式碼
txt

# 將 txt 變數中的文字以空格為分隔符進行切分，並取得結果中的第一個元素
tokens <- strsplit(txt, " ")[[1]]

# 列印 tokens 變數的內容
tokens
# [1] "Jeep" "compares" "electric" "Wagoneer" "S" "to" "Tesla's" "Model" "Y" "in" "new" "teaser" "video" "Electrek.co"

# 計算單字數量
num_words <- length(tokens)

# 列印 num_words 變數的內容
num_words
# [1] 13
#===============================================================================

# 第一段程式碼
# remove punctuation
tokens <- gsub("[[:punct:]]", "", tokens)

# 第二段程式碼
tokens

# 第三段程式碼
# convert to lowercase
tokens <- tolower(tokens)

# 第四段程式碼
tokens

# 第五段程式碼
# Remove stopwords
stopwords <- c("the", "a", "an", "and", "or", "but", "on", "in", "at", "to", "for", "with", 
               "of", "by", "as", "is", "are", "was", "were", "be", "been", "am", "will", 
               "can", "could", "would", "should", "has", "have", "had", "do", "does", "did", 
               "it", "its", "they", "their", "them", "he", "his", "she", "her", "we", "our", 
               "us", "you", "your", "i", "my", "me")

tokens <- tokens[!tokens %in% stopwords]

# 第六段程式碼
tokens

#===============================================================================

install.packages("tm")
install.packages("SnowballC")

library(tm)
library(SnowballC)
library(tidyverse)

clean_descriptions <- c(
  "Jeep compares electric Wagoneer S to Tesla’s Model Y in new teaser video Electrek.co",
  "Tesla’s 0.99% APR Financing For Tesla Model Y Stirring Up Consumer Demand + Chevy Equinox EV Potential & Hot Volvo EX30",
  "Here is a possible rendering of the Tesla Model Y Juniper Tesla Magazine"
)

corpus <- Corpus(VectorSource(clean_descriptions))

corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
corpus <- tm_map(corpus, stripWhitespace)

dtm <- DocumentTermMatrix(corpus)
dtm_matrix <- as.matrix(dtm)
dtm_df <- as.data.frame(dtm_matrix)
print(dtm_df)

#===============================================================================

# 第一段程式碼
# save the Document-Term Matrix to a CSV file
write.csv(dtm_df, "bag_of_words.csv", row.names = TRUE)

#===============================================================================

# 第一段程式碼
install.packages("pdftools")
install.packages("Rpoppler")
install.packages("tm", dependencies = TRUE)
install.packages("topicmodels")

# 第二段程式碼
# Load the CSV file
file_path <- "tesla_model_y_news.csv"
news_data <- read.csv(file_path, stringsAsFactors = FALSE)

# 第三段程式碼
# Check the structure of the data
str(news_data)

#===============================================================================

if (!"description" %in% colnames(news_data)) {
  stop("The 'description' column does not exist in the provided CSV file.")
}

stemmed_descriptions <- news_data %>%
  mutate(stemmed_description = sapply(description, function(x) {
    if (!is.na(x)) {
      return(paste(stem_words(unlist(strsplit(x, "\\s+"))), collapse = " "))
    } else {
      return(NA)
    }
  }))

lemmatized_descriptions <- stemmed_descriptions %>%
  mutate(lemmatized_description = sapply(description, function(x) {
    if (!is.na(x)) {
      return(paste(lemmatize_words(unlist(strsplit(x, "\\s+"))), collapse = " "))
    } else {
      return(NA)
    }
  }))

#===============================================================================

# 第一段程式碼
# Print the first few rows of the modified data frame
print(head(lemmatized_descriptions))

#===============================================================================

write.csv(lemmatized_descriptions, "tesla_model_y_news_processed.csv", row.names = FALSE)

#===============================================================================

