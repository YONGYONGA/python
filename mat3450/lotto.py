##################################################project 1번
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import datetime 
import requests
import warnings 
warnings.filterwarnings(action='ignore')
from time import sleep

df=pd.DataFrame()
df[0]=None
df[1]=None
df[2]=None
df[3]=None
df[4]=None
df[5]=None
df[6]=None

df


url2=1    
while True:
    url1='https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo='
    
    url=url1+str(url2)

    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    Find_date= soup.find('p', {'class': 'desc'})
    Find1= soup.find('div', {'class': 'win_result'})       
    Find_date=str(Find_date)

    year=(Find_date.split('(')[1].split(')')[0].split()[0][:4])
    if year == '년':
        break
    year=int(year)
    month=int(Find_date.split('(')[1].split(')')[0].split()[1][:2])
    day=int(Find_date.split('(')[1].split(')')[0].split()[2][:2])
    if month<10:
        month='0'+str(month)
        if day<10:
            day='0'+str(day)
            Days=str(year)+'-'+month+'-'+day
        else:
            Days=str(year)+'-'+month+'-'+str(day)
    else:    
        if day<10:
            day='0'+str(day)
            Days=str(year)+'-'+str(month)+'-'+day
        else:
            Days=str(year)+'-'+str(month)+'-'+str(day)
    
    
    for i in range(0,7) :
        Find2= int(Find1.findAll('span')[i].text)
        df.loc[Days,i]=Find2
        
    print(Days)
        
    url2=url2+1
    if (int(month) == 1)|(int(month) == 3)|(int(month)==5)|(int(month)==7)|(int(month)==9)|(int(month)==11):
        sleep(1)
        

Day=input('yy-MM-dd')
if Day=='':
    cur_time=datetime.datetime.now()
    time=str(cur_time)
    year_input=time[:4];year_input=int(year_input)
    month_input=time[5:7]; month_input=int(month_input)
    day_input=time[8:10]; day_input=int(day_input)
else: 
    year_input,month_input,day_input=Day.split('-')
    year_input=int(year_input)
    month_input=int(month_input)
    day_input=int(day_input)

Days2=datetime.date(year_input, month_input, day_input)
week_number=Days2.weekday() #수요일은 2 일요일은 6 
if week_number > 5: #일요일인 경우에 
    lotto_day = str(Days2 - datetime.timedelta(days=1))
    lotto_day='20'+lotto_day[2:]
elif week_number < 5:
    lotto_day = str(Days2 - datetime.timedelta(days=week_number+2))
    lotto_day='20'+lotto_day[2:]
elif week_number == 5:
    lotto_day='20'+str(Days2)[2:]
lotto_day_number=list(df.index)
if lotto_day not in lotto_day_number:
    lotto_day=lotto_day_number[len(lotto_day_number)-1]
    lotto_day_number=lotto_day_number.index(lotto_day)
else:    
    lotto_day_number=lotto_day_number.index(lotto_day)
    
Select_df=df[:lotto_day_number+1]

for i in range(0,7):
    Select_df.loc['Mean',i]=Select_df[i].mean()
    Select_df.loc['Variance',i]=Select_df[i].var()
    
display(Select_df)
