import pandas as pd

df = pd.read_csv("Philippines.csv")

df = df.drop(columns = ['Unnamed: 0','lol'])

df.to_csv(f'Philippines.csv',index=False)

