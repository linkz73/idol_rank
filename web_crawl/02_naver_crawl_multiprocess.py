import urllib.request
import bs4
from urllib import parse
import pymysql
from multiprocessing import Pool


con = pymysql.connect(host = "localhost", user = "django_app", password ="django_app123",
                      db = "django_app")
cur = con.cursor()


def chart_portal(i, names, dates):
    name_url = urllib.parse.quote_plus(str(names[i]))
    url = 'https://search.naver.com/search.naver?where=news&query=' + name_url + '&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=' \
          + str(dates[i])[:4] + "." + str(dates[i])[4:] + '.01&de=' + str(dates[i])[:4] + "." + str(dates[i])[4:] \
          + '.31&docid=&nso=so%3Ar%2Cp%3Afrom' + str(dates[i]) + '01to' + str(dates[i]) + '31%2Ca%3Aall&mynews=0&refresh_start=0&related=0'

    html = urllib.request.urlopen(url)
    bs_obj = bs4.BeautifulSoup(html, "lxml")

    ul = bs_obj.find("div", {"class":"title_desc all_my"})
    try:
        lis= ul.find("span")
        span = lis.text.split('/')
        wws = span[1]
        wws = wws.replace("건", "").replace(",", "").replace(" ", "")
        result = wws, names[i], dates[i]
        print(result)
        return result
    except:
        result_ex = '0', names[i], dates[i]
        print(result_ex)
        return result_ex
        pass


if __name__ == '__main__':
    data_sql = "select idol_id, chart_date from django_app.temp_chart"
    cur.execute(data_sql)
    datas = cur.fetchall()
    names = []
    dates = []

    for data in datas:
        name = data[0]
        names.append(name)
        date = data[1]
        dates.append(date)
    nrow_sql = "SELECT COUNT(*) FROM django_app.temp_chart;"
    cur.execute(nrow_sql)
    nrow = cur.fetchone()[0]

    result_pool = []
    with Pool(processes=6) as p:
        try:
            res = [p.apply_async(chart_portal, args=(i, names, dates)) for i in range(0,nrow,1)]
            result_pool = [r.get() for r in res]
        except Exception as e:
            print("exceptions is ", e)
            pass

    update_chart_sql = """UPDATE django_app.temp_chart
                        SET chart_portal = %s
                        WHERE idol_id = %s AND chart_date = %s"""
    val = result_pool
    cur.executemany(update_chart_sql,val)
    con.commit()
    
    con.close()