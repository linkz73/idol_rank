import lxml
import pandas as pd
# from sqlalchemy import create_engine
import urllib.request
import bs4
from urllib import parse
from IPython.display import display
import pymysql
from multiprocessing import Pool


con = pymysql.connect(host = "localhost", user = "root", password ="1234",
                      db = "idol_rank")
cur = con.cursor()


def list1(a, names, dates):
    for i in range(a, a+1, 1):
        name_url = urllib.parse.quote_plus(names[i])

        url = 'https://search.naver.com/search.naver?where=news&query=' + name_url + '&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=' \
              + str(dates[i])[:4] + "." + str(dates[i])[4:] + '.01&de=' + str(dates[i])[:4] + "." + str(dates[i])[4:] \
              + '.31&docid=&nso=so%3Ar%2Cp%3Afrom' + str(dates[i]) + '01to' + str(dates[i]) + '31%2Ca%3Aall&mynews=0&refresh_start=0&related=0'

        html = urllib.request.urlopen(url)
        bs_obj = bs4.BeautifulSoup(html, "html.parser")

        ul = bs_obj.find("div", {"class":"title_desc all_my"})
        try:
            lis= ul.find("span")
            span = lis.text.split('/')
            wws = span[1]
            wws = wws.replace("건", "").replace(",", "").replace(" ", "")
            result = wws, names[i], dates[i]
            return result
        except:
            result_ex = '0', names[i], dates[i]
            return result_ex
            pass


if __name__ == '__main__':
    data_sql = "select 아이돌, 날짜 from idol_rank.idol_chart"
    cur.execute(data_sql)
    datas = cur.fetchall()
    names = []
    dates = []

    for data in datas:
        name = data[0]
        names.append(name)
        date = data[1]
        dates.append(date)
    nrow_sql = "SELECT COUNT(*) FROM idol_chart;"
    cur.execute(nrow_sql)
    nrow = cur.fetchone()[0]

    list = []
    with Pool(processes=6) as p:
        res = [p.apply_async(list1, args=(i, names, dates))
               for i in range(0,nrow,1)]
        result_pool = [r.get() for r in res]

    print = result_pool

    # make_sql = "ALTER TABLE idol_chart ADD(Naver_News TEXT);"
    # cur.execute(make_sql)
    # con.commit()
    #
    # insert_sql = "INSERT INTO idol_chart(Naver_News) values " + str(list)
    # cur.execute(insert_sql)
    # con.commit()
    #
    # con.close()