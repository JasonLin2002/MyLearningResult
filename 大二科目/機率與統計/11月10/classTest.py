import scipy.stats as stats
import pandas as pd

data = pd.read_excel('FedEmail.xlsx')

delivery_time = data['Email Sent and Received']

sample_mean = delivery_time.mean()
sample_std = delivery_time.std(ddof=1)  # 使用 Bessel's correction

# 假設檢定的虛無假設（Null Hypothesis）：mu <= 100
# 選擇備择假設（Alternative Hypothesis）：mu > 100
# 假設水準（Significance Level）通常選擇 0.05
alpha = 0.05

t_statistic, p_value = stats.ttest_1samp(delivery_time, 100)

print(f'T-statistic: {t_statistic}')
print(f'P-value: {p_value}')

# 判斷是否拒絕虛無假設
if p_value < alpha:
    print('拒絕零假設，有足夠的證據支持備擇假設：平均時間大於100小時。 ')
else:
    print('未拒絕虛無假設，沒有足夠的證據支持備擇假設：平均時間大於100小時。 ')