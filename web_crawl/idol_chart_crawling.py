from selenium import webdriver
import pandas as pd
from IPython.display import display
import pymysql

con = pymysql.connect(host = "localhost", user = "root", password ="1234",
                      db = "idol_rank")
# conn=engine.connect()
cur = con.cursor()

# selenium 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument("headless") # 속도 개선
# options.add_argument("disable-gpu") # 그래픽 카드 미사용
options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)

df = pd.DataFrame(columns=['순위', 'idol', '음원/음반', '유튜브', '전문가/평점랭킹', '방송/포털/소셜', '총점', '순위변화', '아이돌 평점주기', '날짜', 'img'])
for year in range(2018,2020,1):
    for month in range(1,13,1):
        if year == 2019 and month == 12:
            break
        else:
            total_m = []
            img_list = []
            for page in range(1,6,1):

                url = "https://www.idol-chart.com/ranking/month/?sm="+str(year) +str(month).rjust(2, '0') +"&page=" +str(page)

                driver.get(url)
                driver.implicitly_wait(3)
                items = driver.find_elements_by_tag_name("td")
                spans = driver.find_elements_by_tag_name("span")


                for span in spans:
                    img_url = span.get_attribute("style")
                    if img_url:
                        img_url = img_url.split('\"')
                        img = img_url[1]
                        img = "https://www.idol-chart.com" + img
                        img_list.append(img)

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

            if img_list:
                for i in range(len(result)):
                    result[i].append(str(year) + str(month).rjust(2, '0'))
                    result[i].append(img_list[i])


            sub_df = pd.DataFrame(result, columns=['순위', 'idol', '음원/음반', '유튜브', '전문가/평점랭킹', '방송/포털/소셜', '총점', '순위변화', '아이돌 평점주기', '날짜', 'img'])
            df = df.append(sub_df)

driver.close()

df.drop(['순위','유튜브', '전문가/평점랭킹', '순위변화', '아이돌 평점주기'], axis='columns', inplace=True)
# display(df)
# df = pd.read_csv("id0l_csv")
df_val = df.values.tolist()
# print(df_val)
# print(type(df_val))
# print(df_val[0][1])
# print(type(df_val[0][1]))
# print(df_val[0][6])
# print(type(df_val[0][6]))

create_idol_sql = """CREATE TABLE idol_rank.idol (idol_id INT AUTO_INCREMENT PRIMARY KEY, idol_name VARCHAR(10) UNIQUE, idol_img VARCHAR(1000))"""
cur.execute(create_idol_sql)
con.commit()

insert_idol_sql = """INSERT INTO idol(idol_name, idol_img)
SELECT %s, %s
FROM dual
WHERE NOT EXISTS (SELECT *  FROM idol
WHERE  idol_name = %s)"""

val = [(df_val[i][1], df_val[i][6],df_val[i][1]) for i in range(len(df_val))]

# print(val)
cur.executemany(insert_idol_sql,val)
con.commit()
con.close()
# df_idol = df.loc[:,['idol','img']]
# df_chart = df.loc[:,['idol','음원/음반','방송/포털/소셜', '총점','날짜']]
# idol_name = df_idol.loc[1,['idol']]
