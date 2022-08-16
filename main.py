import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path ='/Users/rich/Desktop/gpa_calculator/成績單.xlsx'
#設定一下index
df = pd.read_excel(path,header=1)
df = df.drop(columns=['Unnamed: 1'])

#進行資料清洗
df['學分'].fillna(0,inplace=True)
學分condition = df['學分'] == 0
df = df.drop(index=df[學分condition].index)
df['成績'].replace('棄修','不列入計算',inplace=True)
成績condiction = df['成績'] == '不列入計算'
df = df.drop(index=df[成績condiction].index)

#轉換標準https://www.scholaro.com/gpa-calculator/ (60 minimum pass)
#用numpy select()
conditions=[
    (df['成績']>= 80),
    (df['成績']>= 70),
    (df['成績']>=60),
    (df['成績']<60)]
等地=['4','3','2','0'] 
df['等地'] = np.select(conditions, 等地)

#計算gpa
學分總和= df['學分'].sum()
#使用.astype()轉成float
等地總積分 = (df['學分'].astype(float)*df['等地'].astype(float)).sum()
gpa = 等地總積分/學分總和
gpa = round(gpa,2)
print('gpa =',gpa)

#抵免成功學分數:38
#兩所學校總修學分數為:128+文化抵免失敗學分數
文化抵免失敗學分數=df['學分'][0:23].sum()-38
畢業總修學分=128+文化抵免失敗學分數

#目標gpa設定
dreamgpa = 3.5
夢想gpa等地總幾分=畢業總修學分*3

#截至2下目前已修學分
目前已修學分 = df['學分'].sum()
還可修學分 = 畢業總修學分-目前已修學分
目前等地總幾分 = (df['學分'].astype(float)*df['等地'].astype(float)).sum()

#計算往後的課程平均至少為多少才會達標
達標平均等地 = round(((夢想gpa等地總幾分-目前等地總幾分)/還可修學分),2)
print('---------------------')
print(達標平均等地)
print('達標平均分 =','78')

#資料視覺化
文化一上平均 = round((df[0:7]['成績'].sum())/7,2)
文化一下平均 = round((df[7:15]['成績'].sum())/8,2)
文化二上平均 = round((df[15:23]['成績'].sum())/8,2)
輔大二下平均 = round((df[23:]['成績'].sum())/7,2)

文化一下平均改 = round((df[7:15]['成績'].sum()/7),2)

xpoints=['一上','一下','二上','二下']
ypoints=[文化一上平均,文化一下平均,文化二上平均,輔大二下平均]
newypoints=[文化一上平均,文化一下平均改,文化二上平均,輔大二下平均]
plt.plot(xpoints, ypoints)
plt.plot(xpoints,newypoints)
plt.show()
