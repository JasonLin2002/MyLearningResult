play_data <- read.csv("C:\\Users\\jk121\\Documents\\Code\\learning-result\\大數據分析與應用\\0509\\DTree.csv", header = TRUE, sep = ",")

summary(play_data)

play_data

#=============================================================================
library(rpart)
play_DTree <- rpart(Play ~ ., 
                 data = play_data,
                 method = "class",
                 control = rpart.control(minsplit = 1),
                 parms = list(split = "information"))

summary(play_DTree)

#=============================================================================
install.packages("rpart.plot")

library(rpart.plot)

pdf("Play_DT.pdf", width = 8, height = 6)
rpart.plot(play_DTree, type = 4, extra = 1, main = "Decision Tree for Play Data")
dev.off()

#=============================================================================
library(rpart)

play_DTree_gini <- rpart(Play ~ ., 
                         data = play_data, 
                         method = "class",
                         control = rpart.control(minsplit = 1),
                         parms = list(split = "gini"))

summary(play_DTree_gini)

pdf("./Play_DT_2.pdf", width = 8, height = 6)
rpart.plot(play_DTree_gini, type = 4, extra = 2, clip.right.labs = FALSE, 
           varlen = 0, faclen = 0, cex = 0.8, 
           main = "Decision Tree for Play Data")
dev.off()