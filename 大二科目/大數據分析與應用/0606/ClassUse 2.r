install.packages("BiocManager")  # 安裝BiocManager套件
BiocManager::install("Biobase")  # 使用BiocManager安裝Biobase套件
install.packages("NMF")  # 安裝NMF套件

library(NMF)  # 載入NMF函式庫

V <- matrix(c(1, 1, 1, 1, 0, 0,  # 文件1的詞彙向量
              1, 1, 1, 0, 1, 0,  # 文件2的詞彙向量
              0, 0, 0, 1, 1, 1), # 文件3的詞彙向量
            nrow = 3, ncol = 6, byrow = TRUE)  # 定義矩陣的維度和排列方式

nmf_result <- nmf(V, 2, seed = "random")  # 套用NMF模型，設置主題數量為2，隨機種子

W <- basis(nmf_result)  # 提取基矩陣W
H <- coef(nmf_result)  # 提取係數矩陣H

options(digits = 4, scipen = 100)  # 設置數字顯示精度和科學計數法閾值

print("Document-Topic Matrix (W):")  # 打印文件-主題矩陣W
print(W)  # 顯示矩陣W
print("Topic-Term Matrix (H):")  # 打印主題-詞彙矩陣H
print(H)  # 顯示矩陣H

#===============================================================================

