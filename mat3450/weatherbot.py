################################################# project 2번
import telepot 
import os 
import logging #log 라이브러리
import requests
from bs4 import BeautifulSoup
import time
from pandas import DataFrame
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

genietoken ="5694476353:AAH-w9gBLCZg1o1is643QtDZ4VnDIG4nI-Y"
bot=telepot.Bot(genietoken)
InfoMsg="\n1.향후 12시간 날씨 \n2.향후 12시간 강수\n3.향후 12시간 바람\n4.향후 12시간 습도\n5.주간예보\n6.관련기사\n7.종료\n\n기본정보를 다시보기 원하시면 '*'\n즉시 종료를 원하시면 'bye'를 입력해주세요."

status=True
def n_weather_crawling(where):
    url="https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={}날씨".format(where)
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')
    #print(soup)
    weather=""
    first_info=soup.select("div.temperature_info")
    second_info=soup.select("ul.today_chart_list>li>a>span")
    if len(first_info) and len(second_info)>0:
        oo=soup.select("div._today>div>div>strong")
        one=soup.select("div.temperature_info>p.summary")
        my_temp=soup.select("div.temperature_info>dl.summary_list>dd.desc")
        for_wind=soup.select("div.temperature_info>dl.summary_list>dt.term")
        if len(one) >0 and len(my_temp)>0 and len(for_wind)>0:
             ot=oo[0].text.strip()
             one=one[0].text.strip()
             chegam=my_temp[0].text.strip()
             water=my_temp[1].text.strip()
             wind=my_temp[2].text.strip()
             where_wind=for_wind[2].text.strip()
             mise=second_info[0].text.strip()
             chomise=second_info[1].text.strip()
             ssun=second_info[2].text.strip()
             
             sunset=second_info[3].text.strip()
             if(int(sunset[0:2])<12):
                 se="일출"
             else:
                 se="일몰"
             weather="{}C\r\n{}\r\n체감온도 : {}\r\n습도 : {}\r\n{} : {}".format(ot,one,chegam,water,where_wind,wind)
             weather=weather+"\r\n미세먼지 : {}\r\n초미세먼지 : {}\r\n자외선 : {}\r\n{} 시간 : {}".format(mise,chomise,ssun,se,sunset)
    if(weather==""):
        weather="잘못된 지역입니다."
    return weather
def after_12_water(where):
    url="https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={}날씨".format(where)
    r=requests.get(url)
    percent=[]
    waters=[]
    times=[]
    soup=BeautifulSoup(r.text,'html.parser')
    go=soup.select("div.climate_box")
    result=""
    s=0
    if(len(go)>0):
        sese=soup.select("div.scroll_box._horizontal_scroll._hourly_rain>div>div.climate_box>div.icon_wrap>ul>li>em")
        tete=soup.select("div.climate_box>div.graph_wrap>ul>li>div")
        soso=soup.select("div.climate_box>div.time_wrap>ul>li>span")
        #print(soso)
        if(len(sese)>0 and len(tete)>0 and len(soso)>0):
            for i in range(12):
                percent.append(sese[i].text.strip())
                if(sese[i].text.strip()=="-"):
                   percent[i]="0%"
                #if(percent[i][-1]!="%"):
                 #   percent[i]+="%"
            for i in range(12):
                 waters.append(tete[i].text.strip())   
                 s+=int(waters[i])
                 waters[i]+="mm"
                 
            for i in range(12):
                times.append(soso[i].text.strip())
                if(soso[i].text.strip()=="내일"):
                   times[i]="00시"     
            result="        {:<8}{:<8}\r\n".format("강수확률(%)","강수량(mm)")
            for i in range(12):
                result+="{:<4} {:>15} {:>15}\r\n".format(times[i],percent[i],waters[i])
                if(i==11):
                    result+="평균 강수량 : {:.2f}mm".format(s/12)
            #dict={"강수확률(%)":percent,"강수량(mm)" :waters}
            r#esult=str(DataFrame(dict,columns=["강수확률(%)","강수량(mm)"],index=times))
    return result   
def after_12_weather(where):
    url="https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={}날씨".format(where)
    r=requests.get(url)
    times=[]
    wes=[]
    gion=[]
    soup=BeautifulSoup(r.text,'html.parser')
    go=soup.select("div.graph_inner._hourly_weather")
    result=""
    s=0
    if(len(go)>0):
        sese=soup.select("div.graph_inner._hourly_weather>ul>li>dl>dt>em")
        tete=soup.select("div.graph_inner._hourly_weather>ul>li>dl>dd.weather_box>i>span")

        soso=soup.select("div.graph_inner._hourly_weather>ul>li>dl>dd.degree_point>div>div>span")
        #print(soso)
        if(len(sese)>0 and len(tete)>0 and len(soso)>0):
            for i in range(12):
                times.append(sese[i].text.strip())
                if(sese[i].text.strip()=="내일"):
                   times[i]="00시"
            for i in range(12):
                 wes.append(tete[i].text.strip())   
            for i in range(12):
                 gion.append(soso[i].text.strip())
                 s+=int(gion[i][:-1])
                 gion[i]+='C'      
            result="        {:>8}{:>8}\r\n".format("날씨","기온")
            for i in range(12):
                result+="{:<4}{:>10}{:>15}\r\n".format(times[i],wes[i],gion[i])
                if(i==11):
                    result+="평균 기온 : {:.2f}C".format(s/12)                 
            #dict={"날씨__":wes,"_기온_" :gion}
            #result=str(DataFrame(dict,columns=["날씨__","_기온_"],index=times))
            
    return result
def after_12_spdo(where):
    url="https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={}날씨".format(where)
    r=requests.get(url)
    waters=[]
    times=[]
    soup=BeautifulSoup(r.text,'html.parser')
    go=soup.select("div.humidity_graph_box")
    result=""
    s=0
    if(len(go)>0):
        sese=soup.select("div.humidity_graph_box>div>div>div>div.graph_wrap>ul>li>div>span>span")
        soso=soup.select("div.humidity_graph_box>div>div>div>div.time_wrap>ul>li>span")
        if(len(sese)>0  and len(soso)>0):
            for i in range(12):
                waters.append(sese[i].text.strip())
                s+=int(waters[i])
                waters[i]+="%"
            for i in range(12):
                times.append(soso[i].text.strip())
                if(soso[i].text.strip()=="내일"):
                   times[i]="00시"     
            dict={"      습도(%)":waters}

            result=str(DataFrame(dict,columns=["      습도(%)"],index=times))
            result+="\r\n평균습도 : {:.2f}%".format(s/12)
    return result
def after_12_wind(where):
    url="https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={}날씨".format(where)
    r=requests.get(url)
    towind=[]
    pwwind=[]
    times=[]
    soup=BeautifulSoup(r.text,'html.parser')
    go=soup.select("div.wind_graph_box")
    result=""
    s=0
    if(len(go)>0):
        sese=soup.select("div.wind_graph_box>div>div>div>div.icon_wrap>ul>li>em")

        tete=soup.select("div.wind_graph_box>div>div>div>div.graph_wrap>ul>li>div>span>span")
        soso=soup.select("div.wind_graph_box>div>div>div>div.time_wrap>ul>li>span")
        if(len(sese)>0 and len(tete)>0 and len(soso)>0):
            for i in range(12):
                towind.append(sese[i].text.strip())
            for i in range(12):
                 pwwind.append(tete[i].text.strip()) 
                 s+=int(pwwind[i])
                 pwwind[i]+="m/s"
            for i in range(12):
                times.append(soso[i].text.strip())
                if(soso[i].text.strip()=="내일"):
                   times[i]="00시"     
            result="        {:>8}         {:>8}\r\n".format("풍향","풍속(m/s)")
            for i in range(12):
                result+="{:<4}{:>10}{:>15}\r\n".format(times[i],towind[i],pwwind[i])
                if(i==11):
                    result=result+"평균 풍속 : {:.2f}m/s".format(s/12)              
            #dict={"_풍향":towind,"풍속(m/s)" :pwwind}

            #result=str(DataFrame(dict,columns=["_풍향","풍속(m/s)"],index=times))
    return result    
def news_4(where):
    url="https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={}날씨".format(where)
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')
    go=soup.select("div.group_news")
    result=""
    c=1
    if(len(go)>0):
        one=soup.select("#sp_nws_all1>div.news_wrap.api_ani_send>div>a")[0]['title']
        onelink=soup.select("#sp_nws_all1>div.news_wrap.api_ani_send>div>a")[0]['href']
        if(len(one)>0):
            result+="{}번째 뉴스 : {}\r\n링크: {}".format(c,one,onelink)
            c+=1
        two=soup.select("ul.list_news>li.bx>div.news_wrap.api_ani_send>div>a")[1]['title']
        twolink=soup.select("ul.list_news>li.bx>div.news_wrap.api_ani_send>div>a")[1]['href']
        if(len(two)>0):
            result+="\r\n\n{}번째 뉴스 : {}\r\n링크: {}".format(c,two,twolink)
            c+=1
        three=soup.select("ul.list_news>li.bx>div.news_wrap.api_ani_send>div>a")[2]['title']
        threelink=soup.select("ul.list_news>li.bx>div.news_wrap.api_ani_send>div>a")[2]['href']
        if(len(three)>0):
            result+="\r\n\n{}번째 뉴스 : {}\r\n링크: {}".format(c,three,threelink)
            c+=1
        four=soup.select("ul.list_news>li.bx>div.news_wrap.api_ani_send>div>a")[3]['title']
        fourlink=soup.select("ul.list_news>li.bx>div.news_wrap.api_ani_send>div>a")[3]['href']
        if(len(four)>0):
            result+="\r\n\n{}번째 뉴스 : {}\r\n링크: {}".format(c,four,fourlink)
            c+=1
   # print(result)       
    return result   
def week_weather(where):
    url="https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={}날씨".format(where)
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')
    go=soup.select("div.weekly_forecast_area._toggle_panel")
    result=""
    datas=[]
    days=[]
    mornig_we=[]
    night_we=[]
    h_l_temp=[]
    hh_temp=[]
    """for i in range(10):
            wh.append(yuhu[i].text.strip())
        for i in range(10):
            print(wh[i]) """
    if(len(go)>0):
        yoho=soup.select("div.weekly_forecast_area._toggle_panel>div.list_box._weekly_weather>ul>li>div>div>span>strong")
      #  print(yoho)
        for i in range(10):
            datas.append(yoho[i].text.strip())        
        yuhu=soup.select("div.weekly_forecast_area._toggle_panel>div.list_box._weekly_weather>ul>li>div>div>span>span.date")
        for i in range(10):
            #datas[i]+="\n{}".format(yuhu[i].text.strip())
            days.append(yuhu[i].text.strip()) 
        m=soup.select("div.weekly_forecast_area._toggle_panel>div.list_box._weekly_weather>ul>li>div>div.cell_weather>span>span>span.rainfall")
        for i in range(10):
            mornig_we.append(m[i*2].text.strip()) 
            night_we.append(m[i*2+1].text.strip()) 
            
        f=soup.select("div.weekly_forecast_area._toggle_panel>div.list_box._weekly_weather>ul>li>div>div.cell_weather>span>i>span.blind")
        for i in range(10):
            mornig_we[i]+=" / {}".format(f[i*2].text.strip())
            night_we[i]+=" / {}".format(f[i*2+1].text.strip())
        final=soup.select("div.weekly_forecast_area._toggle_panel>div.list_box._weekly_weather>ul>li>div>div.cell_temperature>span>span.lowest")

        for i in range(10):
            h_l_temp.append(final[i].text.strip())
        for i in range(10):
            h_l_temp[i]="{0:>3}C".format(h_l_temp[i][4:])

        tfinal=soup.select("div.weekly_forecast_area._toggle_panel>div.list_box._weekly_weather>ul>li>div>div.cell_temperature>span>span.highest")
        #for i in range(10):
            #kk=tfinal[i].text.strip()
            #kk="{0:>3}C".format(kk[4:])
            #h_l_temp[i]+=kk
        for i in range(10):
            hh_temp.append(tfinal[i].text.strip())
        for i in range(10):
            hh_temp[i]="{0:>3}C".format(hh_temp[i][4:])    
        if(len(datas)>0 and len(night_we)>0 and len(h_l_temp)>0):
            result="{:<5}  {:>8}   {:>8}\r\n".format("날짜","(강수/날씨)"," 최저.최고기온")
            for i in range(10):
                result+="{:<4}(오전){:>10}{:>15}\r\n".format(datas[i],mornig_we[i],h_l_temp[i])
                result+="{:<4}(오후){:>10}{:>15}".format(days[i][:-1],night_we[i],hh_temp[i])
                
                if(i!=9):
                    result+="\r\n\r\n"   
            #dict={"오전(강수/날씨)":mornig_we,"오후(강수/날씨)" :night_we,"최저/최고 온도":h_l_temp}

         #   result=str(DataFrame(dict,columns=["오전(강수/날씨)","오후(강수/날씨)","최저/최고 온도" ],index=datas))
    #print(result)
    return result   
def handle(msg):
    global weather_on
    global WHere
    content,chat,id=telepot.glance(msg)
    print(content,chat,id)
    if content=='text':
        strd=msg["text"]
        args=strd.split(" ")
        command=args[0]
        if(command=='2' and weather_on==0 and WHere==""):
            bot.sendMessage(id, "종료하겠습니다.")
            os._exit(1)    
        elif(WHere=="" and weather_on==0):
            if(command.isdigit()!=True and command!=""):
                bot.sendMessage(id, "{}의 날씨 검색중...".format(command))
                www=n_weather_crawling(command)

            else:
                www="잘못된 지역입니다."
                bot.sendMessage(id, www)
            if(www=="잘못된 지역입니다."):
                bot.sendMessage(id, www)
                bot.sendMessage(id, "날씨를 알고싶은 지역을 입력하세요. 2번을 누를시 종료됩니다.")
            else:
                bot.sendMessage(id, www)
                WHere=command
                weather_on=2
                bot.sendMessage(id, "{}날씨 더 많은 정보\n".format(WHere)+InfoMsg)
        elif(command=='1' and weather_on==2):
            bot.sendMessage(id, "향후 12시간 날씨 확인중..")
            after_www=after_12_weather(WHere)
            if(after_www==""):
                bot.sendMessage(id, "죄송합니다. 검색에 실패했습니다. 다시 시도해주세요.")
            else:
                bot.sendMessage(id, "{}의 향후 12시간 날씨\r\n".format(WHere)+after_www)
        elif(command=='2' and weather_on==2):
            bot.sendMessage(id, "향후 12시간 강수 확인중..")
            after_www=after_12_water(WHere)
            if(after_www==""):
                bot.sendMessage(id, "죄송합니다. 검색에 실패했습니다. 다시 시도해주세요.")
            else:
                bot.sendMessage(id, "{}의 향후 12시간 강수\r\n".format(WHere)+after_www)
        elif(command=='3' and weather_on==2):
            bot.sendMessage(id, "향후 12시간 바람 확인중..")
            after_www=after_12_wind(WHere)
            if(after_www==""):
                bot.sendMessage(id, "죄송합니다. 검색에 실패했습니다. 다시 시도해주세요.")
            else:
                bot.sendMessage(id, "{}의 향후 12시간 바람정보\r\n".format(WHere)+after_www)
        elif(command=='4' and weather_on==2):
            bot.sendMessage(id, "향후 12시간 습도 확인중..")
            after_www=after_12_spdo(WHere)
            if(after_www==""):
                bot.sendMessage(id, "죄송합니다. 검색에 실패했습니다. 다시 시도해주세요.")
            else:
                bot.sendMessage(id, "{}의 향후 12시간 습도\r\n".format(WHere)+after_www)
        elif(command=='5' and weather_on==2):
            bot.sendMessage(id, "주간예보 확인중..")
            after_www=week_weather(WHere)
            if(after_www==""):
                bot.sendMessage(id, "죄송합니다. 검색에 실패했습니다. 다시 시도해주세요.")
            else:
                bot.sendMessage(id, "{}의 주간예보\r\n".format(WHere)+after_www)
        elif(command=='6' and weather_on==2):
            bot.sendMessage(id, "{}날씨 관련 기사 확인중..".format(WHere))
            after_www=news_4(WHere)
            if(after_www==""):
                bot.sendMessage(id, "죄송합니다. 검색에 실패했습니다. 다시 시도해주세요.")
            else:
                bot.sendMessage(id, "{}의 대표 관련기사 4개\r\n".format(WHere)+after_www)
        elif(command=='7' and weather_on==2):
            bot.sendMessage(id, "{}날씨 검색을 종료합니다.".format(WHere))
            weather_on=0
            WHere=""
            bot.sendMessage(id, "날씨를 알고싶은 지역을 입력하세요. 2번을 누를시 종료됩니다.")
        elif(command=='bye' and weather_on==2):
            bot.sendMessage(id, "즉시종료합니다! bye!")
            os._exit(1)
        elif(command=='*' and weather_on==2): 
            bot.sendMessage(id, "{}의 기본날씨 정보 재검색중...".format(WHere))
            www=n_weather_crawling(command)
            if(www=="잘못된 지역입니다."):
                bot.sendMessage(id, "죄송합니다. 검색에 실패했습니다. 다시 시도해주세요.")
            else:
                bot.sendMessage(id, www)
        else:
            bot.sendMessage(id, "틀린 옵션입니다")
            if(weather_on==0):
                bot.sendMessage(id, "날씨를 알고싶은 지역을 입력하세요. 2번을 누를시 종료됩니다.")
            elif(weather_on==2 and WHere!=""):
                bot.sendMessage(id, "{}날씨 더 많은 정보\n".format(WHere)+InfoMsg)
            else:
                dummy=0
bot.message_loop(handle)
weather_on=0
WHere=""
chat_id='5950141716'
bot.sendMessage(chat_id, "HI!\n날씨를 알고싶은 지역을 입력하세요. 2번을 누를시 종료됩니다.")
while status==True:
    time.sleep(10)              
