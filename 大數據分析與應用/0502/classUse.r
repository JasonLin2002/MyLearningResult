library(ISLR)
data <- Default

summary(data)
data[1:5, ]
nrow(data)

install.packages("ggplot2")
library("ggplot2")

# plot default rate by student status
ggplot(data, aes(x = student)) +
    geom_bar(aes(fill = default), position = position_stack()) +
    theme(legend.position = "top")

set.seed(1)
sample <- sample(c(TRUE, FALSE), nrow(data), replace=TRUE, prob=c(0.7, 0.3))
train <- data[sample, ]
test <- data[!sample, ]
nrow(train)  # 6964
nrow(test)   # 3036

train[1:5, ]
test[1:5, ]

model <- glm(default ~ student + balance + income, family = "binomial", data = train)
options(scipen=999)
summary(model)

library(pscl)
pR2(model)["McFadden"]

library(caret)
varImp(model)

install.packages("carData")
library(car)
vif(model)
