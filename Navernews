import pandas as pd
from sqlalchemy import create_engine
import urllib.request
import bs4
from urllib import parse
import pymysql
import numpy as np

engine = create_engine('mysql+pymysql://root:1234@localhost/idol_rank', convert_unicode=True)
conn=engine.connect()

data = pd.read_sql_table('idol_chart', conn)
# print(data.head())
# print(data)


for i in range(100,4184,1):
    dfname=pd.DataFrame(data, columns= ["아이돌"],index=[i])

    df=pd.DataFrame(data, columns= ["날짜"],index=[i])

    dfnum=pd.DataFrame(data, columns= ["순위"])

    daname = str(dfname.values)
    daname = daname.replace("[['","")
    daname = daname.replace("']]","")
    print(daname)
    #이름 추출

    date = str(df.values)
    date = date.replace("[['","")
    date = date.replace("']]","")
    date=date[0:4]+'.'+date[-2:]


    query = { 'query' : daname }
    ss=parse.urlencode(query, encoding='UTF-8', doseq=True)


    url = 'https://search.naver.com/search.naver?where=news&' + ss + '&sm=tab_opt&sort=1&photo=0&field=0&reporter_article=&pd=3&ds=' + str(date).rjust(2, "0") + '.01&de=' + str(date).rjust(2, "0") + '.31&docid=&nso=so%3Add%2Cp%3Afrom20180101to20180131%2Ca%3Aall&mynews=0&refresh_start=0&related=0'
    print(url)


    html = urllib.request.urlopen(url)
        # print(url)
    bs_obj = bs4.BeautifulSoup(html, "html.parser")

    ul = bs_obj.find("div", {"class":"title_desc all_my"})
    lis= ul.find("span")
    eww=lis.text[7:-1]
    result=eww.replace(",","")

    print(eww.replace(",",""))

