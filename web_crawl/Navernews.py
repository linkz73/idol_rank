import pandas as pd
from sqlalchemy import create_engine
import urllib.request
import bs4
from urllib import parse
from IPython.display import display
import pymysql.cursors

engine = create_engine('mysql+pymysql://root:1234@localhost/idol_rank', convert_unicode=True)
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db='idol_rank', charset='utf8')
conn=engine.connect()

with db.cursor() as cursor:
    sql = "SELECT COUNT(*) as cnt FROM idol_chart;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row_data in result:
        print(type(row_data))
        nrow = row_data[0]
db.close()

data = pd.read_sql_table('idol_chart', conn)
# print(data.head())
# print(data)
list = []
for i in range(1,nrow,1):
    dfname=pd.DataFrame(data, columns= ["아이돌"],index=[i])

    df=pd.DataFrame(data, columns= ["날짜"],index=[i])

    dfnum=pd.DataFrame(data, columns= ["순위"])

    daname = str(dfname.values)
    daname = daname.replace("[['","")
    daname = daname.replace("']]","")

    #이름 추출

    date = str(df.values)
    date = date.replace("[['","")
    date = date.replace("']]","")
    date=date[0:4]+'.'+date[-2:]


    query = { 'query' : daname }
    ss=parse.urlencode(query, encoding='UTF-8', doseq=True)

    url = 'https://search.naver.com/search.naver?where=news&' + ss + '&sm=tab_opt&sort=1&photo=0&field=0&reporter_article=&pd=3&ds=' + str(date).rjust(2, "0") + '.01&de=' + str(date).rjust(2, "0") + '.31&docid=&nso=so%3Add%2Cp%3Afrom20180101to20180131%2Ca%3Aall&mynews=0&refresh_start=0&related=0'


    html = urllib.request.urlopen(url)
    bs_obj = bs4.BeautifulSoup(html, "html.parser")

    ul = bs_obj.find("div", {"class":"title_desc all_my"})
    try:
        lis= ul.find("span")
        span = lis.text.split('/')
        wws = span[1]
        result = wws.replace("건", "").replace(",", "")
        list.append(result)
    except:
        list.append('0')

df = pd.DataFrame(list, columns=['Naver뉴스'])
df_c = pd.merge(data, df, how='right')

df_c.to_excel('test_last.xlsx', sheet_name = 'sheet1')
display(df_c)
