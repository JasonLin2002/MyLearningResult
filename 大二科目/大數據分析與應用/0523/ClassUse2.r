library(forecast)

data("AirPassengers")
ts_data <- AirPassengers

plot(ts_data)

#==============================================================================

ndiffs(ts_data)  # Determine the number of differences needed
diff_ts_data <- diff(ts_data, differences = 1)  # Apply differencing

plot(diff_ts_data)

#==============================================================================

arima_model <- auto.arima(ts_data)
summary(arima_model)

#==============================================================================

forecasted_values <- forecast(arima_model, h = 12)  # Forecast for the next 12 periods
plot(forecasted_values)

#==============================================================================

# 確認 model_order 的內容
model_order <- arima_model$order
coefficients <- coef(arima_model)

# 打印 ARIMA 訂單
cat("ARIMA Order (p, d, q):\n")
cat("p =", model_order[1], "\n")
cat("d =", model_order[2], "\n")
cat("q =", model_order[3], "\n")

# 打印季節性成分（如果存在）
if (length(model_order) >= 7 && model_order[5] > 0) {
  cat("Seasonal AR (P):", model_order[4], "\n")
  cat("Seasonal D:", model_order[5], "\n")
  cat("Seasonal MA (Q):", model_order[6], "\n")
}

# 打印係數
cat("\nModel Coefficients:\n")
print(coefficients)
