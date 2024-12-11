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