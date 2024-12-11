import pandas as pd

data_set = pd.read_csv("統計學\10月20\iris.csv")
df = pd.DataFrame(data_set)

print(df.describe())