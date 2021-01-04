import pandas as pd

df=pd.read_csv("/home/tubi/Desktop/DetectFakeTrueNews/KullanilacakVeriler/LabelsizVeri/dogru.csv")
df["Label"]=1
df.to_csv("/home/tubi/Desktop/DetectFakeTrueNews/KullanilacakVeriler/LabelliVeri/dogru1.csv",index=False)