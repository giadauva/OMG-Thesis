import pandas as pd

#%%
df1=pd.read_csv("datasets/Dataset 1 UVA .csv", on_bad_lines='skip')
print(df1.head())

#%%
df2 = pd.read_excel("datasets/DATSET 2 UVA lijst mailings.xlsx")
print(df2.head())

#%%
print(df1.columns)
print(df1.dtypes)
print(df1.shape)

#%%
print(df2.columns)
print(df2.dtypes)
print(df2.shape)