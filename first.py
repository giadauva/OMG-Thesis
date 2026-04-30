import pandas as pd

df1=pd.read_csv("datasets/Dataset 1 UVA .csv", on_bad_lines='skip', encoding='latin1')
print(df1.head())

df2 = pd.read_excel("datasets/DATSET 2 UVA lijst mailings.xlsx")
print(df2.head())