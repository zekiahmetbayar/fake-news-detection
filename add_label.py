import pandas as pd

df=pd.read_csv("output.csv")
df["Label"]=1
df.to_csv("output.csv",index=False)