import time
from selenium.webdriver import Chrome
import pandas as pd
from IPython.display import display
from sqlalchemy import create_engine
import pymysql
webdriver = "chromedriver.exe"



driver = Chrome(webdriver)
df = pd.DataFrame(columns=['순위', '아이돌', '음원/음반', '유튜브', '전문가/평점랭킹', '방송/포털/소셜', '총점', '순위변화', '아이돌 평점주기', '날짜'])
for year in range(2018,2020,1):
    for month in range(1,13):
        if year == 2019 and month == 12:
            break
        else:
            total_m = []
            for page in range(1,6):

                url = "https://www.idol-chart.com/ranking/month/?sm="+str(year) +str(month).rjust(2, '0') +"&page=" +str(page)

                driver.get(url)
                time.sleep(3)
                items = driver.find_elements_by_tag_name("td")


                for item in items:
                    if item != None:
                        split_item = []
                        split_item.append(item.text)
                        result = list(map(lambda x: x.replace(',', "").replace(' ', ''), split_item))
                        total_m.append(result)
                    # print(result)
                    # total.append(result)
                    # sub = []
                    # for i in split_item:
                    #     sub.append(i.replace(",",""))
                    # total.append(sub)
                # del total[0]
                # 이중 리스트의 모양을 flatten 하게 하는 함수
            total_m = sum(total_m, [])
                # 일정한 크기로 나눠주는 함수
            n = 9
            result = [total_m[i * n:(i + 1) * n] for i in range((len(total_m) + n - 1) // n)]
                # print(result)
            for i in range(len(result)):
                result[i].append(str(year)+str(month).rjust(2, '0'))
            sub_df = pd.DataFrame(result, columns=['순위', '아이돌', '음원/음반', '유튜브', '전문가/평점랭킹', '방송/포털/소셜', '총점', '순위변화', '아이돌 평점주기', '날짜'])
            df = df.append(sub_df)

driver.close()

df.drop(['유튜브', '전문가/평점랭킹', '순위변화', '아이돌 평점주기'], axis='columns', inplace=True)
display(df)

df.to_excel('test_final.xlsx', sheet_name = 'sheet1')
engine = create_engine("mysql+pymysql://root:"+"1234"+"@127.0.0.1:3306/idol_rank?charset=utf8", encoding='utf-8')
conn = engine.connect()
df.to_sql(name='idol_chart', con=engine, if_exists='append', index = False)
conn.close()