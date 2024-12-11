library("ggplot2")

# 讀取鑽石資料
data("diamonds")

# 選擇切工為 "Premium" 或 "Ideal" 的鑽石
niceDiamonds <- diamonds[diamonds$cut == "Premium" | diamonds$cut == "Ideal", ]

# 繪製密度圖
ggplot(niceDiamonds, aes(x = price, fill = cut)) +
  geom_density(alpha = .3, color = NA)