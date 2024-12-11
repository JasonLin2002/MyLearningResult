install.packages("pdftools")
install.packages("Rpoppler")
install.packages("tm", dependencies = TRUE)
install.packages("topicmodels")

library(tm)
library(topicmodels)

documents <- c(
  "The quick brown fox jumps over the lazy dog",
  "Never jump over the lazy dog quickly",
  "The quick brown fox is quick and smart",
  "Dogs are lazy and love to sleep",
  "Foxes are quick and clever animals"
)

corpus <- VCorpus(VectorSource(documents))

corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
corpus <- tm_map(corpus, stripWhitespace)

dtm <- DocumentTermMatrix(corpus)

dtm

#===============================================================================

num_topics <- 2  # 設定主題數量為2

lda_model <- LDA(dtm, k = num_topics, control = list(seed = 1234))  # 套用LDA模型，設定主題數量和隨機種子

topics <- terms(lda_model, 6)  # 獲取每個主題的前6個詞彙
print(topics)  # 打印主題詞彙

topic_distribution <- posterior(lda_model)$topics  # 獲取每個文件的主題分布
print(topic_distribution)  # 打印主題分布

