from selenium import webdriver
import pandas as pd
import os
# from IPython.display import display #데이터 프레임을 볼 때 사용하는 모듈
import pymysql

con = pymysql.connect(host = "localhost", user = "django_app", password ="django_app123",
                      db = "django_app")
cur = con.cursor()

# selenium 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument("headless") # 속도 개선
# options.add_argument("disable-gpu") # 그래픽 카드 미사용
options.add_argument('window-size=1920x1080')

# OS 디렉터리 경로명을 가져옴
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, 'web_crawl/chromedriver.exe')

driver = webdriver.Chrome(path, chrome_options=options)

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

                #이미지 링크 추출
                for span in spans:
                    img_url = span.get_attribute("style")
                    if img_url:
                        img_url = img_url.split('\"')
                        img = img_url[1]
                        img = "https://www.idol-chart.com" + img
                        img_list.append(img)
                
                #이미지 링크를 제외한 나머지 데이터 추출
                for item in items:
                    if item != None:
                        split_item = []
                        split_item.append(item.text)
                        result = list(map(lambda x: x.replace(',', "").replace(' ', ''), split_item))
                        total_m.append(result)

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
df_val = df.values.tolist()

#idol 테이블 생성
# create_idol_sql = """CREATE TABLE django_app.idol (idol_id INT AUTO_INCREMENT PRIMARY KEY, idol_name VARCHAR(30) UNIQUE, idol_img VARCHAR(1000))"""
# cur.execute(create_idol_sql)
# con.commit()

insert_idol_sql = """INSERT INTO django_app.idol(idol_name, idol_img)
SELECT %s, %s
FROM dual
WHERE NOT EXISTS (SELECT *  FROM django_app.idol
WHERE  idol_name = %s)"""
val = [(df_val[i][0], df_val[i][5],df_val[i][0]) for i in range(len(df_val))]
cur.executemany(insert_idol_sql,val)
con.commit()

#temp_chart 테이블 생성
create_chart_sql = """CREATE TABLE django_app.temp_chart (chart_id INT AUTO_INCREMENT PRIMARY KEY, idol_id VARCHAR(30), chart_music INT,
chart_media INT, chart_portal INT, chart_total INT, chart_date INT)"""
cur.execute(create_chart_sql)
con.commit()

insert_chart_sql = """INSERT INTO django_app.temp_chart(idol_id, chart_music, chart_media, chart_total, chart_date)
VALUES (%s, %s, %s, %s, %s)"""
value = [(df_val[i][0],df_val[i][1],df_val[i][2],df_val[i][3],df_val[i][4])for i in range(len(df_val))]
cur.executemany(insert_chart_sql,value)
con.commit()

con.close()
