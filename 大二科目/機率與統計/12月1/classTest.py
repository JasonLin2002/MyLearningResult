import numpy as np
from scipy.stats import f
import pandas as pd

# Milbank和GulfPark的數據

df = pd.read_excel('Training.xlsx')

milbank_data = df['Current']

gulf_park_data = df['Proposed']

# 計算變異數
var_milbank = np.var(milbank_data, ddof=1)
var_gulf_park = np.var(gulf_park_data, ddof=1)

# 進行F檢定
f_statistic = var_milbank / var_gulf_park
dfn = len(milbank_data) - 1  # Milbank的自由度
dfd = len(gulf_park_data) - 1  # Gulf Park的自由度

# 計算雙尾檢定的P值
p_value = 1-f.cdf(f_statistic, dfn, dfd)

# 輸出結果
print(f"F Statistic: {f_statistic}")
print(f"P-value: {p_value}")

# 判斷假設是否成立
alpha = 0.05
if p_value < alpha:
    print('拒絕虛無假設，即H_a: Var(Milbank) != Var(Gulf Park)')
else:
    print('未能拒絕虛無假設，即H_a: Var(Milbank) = Var(Gulf Park)')
