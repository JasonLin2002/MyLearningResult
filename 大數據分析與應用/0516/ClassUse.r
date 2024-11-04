# Create the time series data
time_series_data <- c(120, 135, 150, 145, 155, 160, 162, 158, 165, 170)

# Convert the data into a time series object
ts_data <- ts(time_series_data)

#==============================================================================

# Load necessary library
library(stats)

# Plotting the Partial Autocorrelation Function (PACF)
pacf(ts_data, main="PACF of Time Series Data")

#==============================================================================

# Define the days and values
days <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
values <- c(120, 135, 150, 145, 155, 160, 162, 158, 165, 170)

# Create a data frame
data <- data.frame(days, values)

# Plot the data
plot(data$days, data$values, type = "p",
     main = "Scatter Plot of Values Over Time",
     xlab = "Day",
     ylab = "Value",
     pch = 19, col = "blue")

# Add lines to the plot
lines(data$days, data$values, col = "red")

#==============================================================================

# Create the time series data
time_series_data <- c(120, 135, 150, 145, 155, 160, 162, 158, 165, 170)

# Convert the data into a time series object
ts_data <- ts(time_series_data)

# Plot the ACF up to lag 5
acf(ts_data, lag.max=5, main="ACF of Time Series Data up to Lag 5")

# Create the time series data
time_series_data <- c(120, 135, 150, 145, 155, 160, 162, 158, 165, 170)

# Convert the data into a time series object
ts_data <- ts(time_series_data)

library(forecast)

# Fit an MA model of order q
q <- 1
ma_model <- Arima(ts_data, order=c(0,0,q), include.mean=TRUE)

# Summary of the model
summary(ma_model)