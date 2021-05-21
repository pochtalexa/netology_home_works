import pandas as pd

df = pd.read_csv('phones.csv', sep=';', index_col=False )

print(df)