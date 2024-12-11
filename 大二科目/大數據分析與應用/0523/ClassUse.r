# Create the time series data
time_series_data <- c(120, 135, 150, 145, 155, 160, 162, 158, 165, 170)

# Convert the data into a time series object
ts_data <- ts(time_series_data)

# Plot the ACF up to lag 5
acf(ts_data, lag.max=5, main="ACF of Time Series Data up to Lag 5")

#==============================================================================

install.packages("forecast")
library(forecast)

# Create the time series data
time_series_data <- c(120, 135, 150, 145, 155, 160, 162, 158, 165, 170)

# Convert the data into a time series object
ts_data <- ts(time_series_data)

# Fit an MA model of order q
q <- 1
ma_model <- Arima(ts_data, order=c(0,0,q), include.mean=TRUE)

# Summary of the model
summary(ma_model)

#==================完全不一樣===============================================

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

