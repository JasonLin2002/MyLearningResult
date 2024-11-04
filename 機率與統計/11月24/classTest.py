import numpy as np
from scipy.stats import chi2
#Times數據
times_data = [
15.7, 16.9, 12.8, 15.6, 14.0, 16.2, 14.8, 19.8, 13.2, 15.3, 14.7, 10.2,
16.7, 13.6, 14.0, 18.2, 15.7, 14.2, 11.1, 16.8, 11.8, 16.0, 14.2, 12.7]
#已知的變異數進行比較
known_variance = 4
#進行卡方檢定
n = len(times_data)
sample_variance = np.var(times_data, ddof=1)
chi_square_statistic = (n - 1) * sample_variance / known_variance
#計算右尾的P值
p_value = chi2.sf(chi_square_statistic, df=n-1)
#翰出結果
print(f"Chi-square statistic: {chi_square_statistic}")
print(f"P-value: {p_value}")