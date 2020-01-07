import urllib.request
import bs4
from urllib import parse

query = { 'query' : '방탄소년단' }
ss=parse.urlencode(query, encoding='UTF-8', doseq=True)


for i in range(1, 13):
    url = 'https://search.naver.com/search.naver?where=news&'+ ss +'&sm=tab_opt&sort=1&photo=0&field=0&reporter_article=&pd=3&ds=2018.' + str(i).rjust(2, "0") + '.01&de=2018.' + str(i).rjust(2,"0") + '.31&docid=&nso=so%3Add%2Cp%3Afrom20180101to20180131%2Ca%3Aall&mynews=0&refresh_start=0&related=0'


    html = urllib.request.urlopen(url)
    # print(url)
    bs_obj = bs4.BeautifulSoup(html, "html.parser")

    ul = bs_obj.find("div", {"class":"title_desc all_my"})
    lis= ul.find("span")
    eww=lis.text[7:-1]

    print(eww.replace(",",""))

