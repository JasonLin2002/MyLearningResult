install.packages("randomForest")

library(randomForest)
library(datasets)
library(ggplot2)
library(caret)

data <- iris
data
data$Species <- as.factor(iris$Species)
table(data$Species)

set.seed(222)
ind <- sample(2, nrow(iris), replace = TRUE, prob = c(0.7, 0.3))
train <- iris[ind==1, ]
test <- iris[ind==2, ]

nrow(train)
nrow(test)

#=============================================================================
rf_model <- randomForest(Species ~ ., data = train, proximity = TRUE)

print(rf_model)

p1 <- predict(rf_model, train)
confusionMatrix(p1, train$Species)

#=============================================================================
p2 <- predict(rf_model, test)

confusionMatrix(p2, test$Species)

#=============================================================================
varImpPlot(rf_model, sort = T, n.var = 10, main = "Variable Importance")

rf_model$importance

#=============================================================================
partialPlot(rf_model, train, Petal.Width, "setosa")
