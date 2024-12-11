import pandas as pd
from scipy.stats import chi2_contingency
#取Excel福案
file_path = 'path to_ your_file.xlsx' #替换為您的案路徑
data = pd.read_excel(file_path)
#創建'Preference'和Gender交叉表
crosstab = pd.crosstab(data['Preference'], data['Gender'])
#進行卡方檢定
chi2, p, dof,expected = chi2_contingency(crosstab)
#翰出結果
print("Chi-square statistic:" chi2)
print("P-value:", p)
print("Degrees of freedom:", dof)
print("Expected frequencies:")
print(expected)
print("InCrosstable:")
print(crosstab)