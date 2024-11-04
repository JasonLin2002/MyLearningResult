import pandas as pd
from scipy import stats

file_path = 'Matched.xlsx'
df = pd.read_excel(file_path)

df['Difference'] = df['Method 1'] - df['Method 2']

t_statistic, p_value = stats.ttest_1samp(df['Difference'], popmean=0)

print(f"t 檢定統計量: {t_statistic:.2f}")
print(f"p-value: {p_value:.3f}")

alpha = 0.05
if alpha < p_value < 0.1:
    print("在 0.05 的顯著水準下，不能拒絕虛無假設 H0。")
else:
    print("在 0.05 的顯著水準下，拒絕虛無假設 H0。")