import time
from selenium.webdriver import Chrome
import pandas as pd
from IPython.display import display


webdriver = "chromedriver.exe"

driver = Chrome(webdriver)
df = pd.DataFrame(columns=['순위', '아이돌', '음원/음반', '유튜브', '전문가/평점랭킹', '방송/포털/소셜', '총점', '순위변화', '아이돌 평점주기', '날짜'])
for year in range(2018,2020,1):
    for month in range(1,3):
        total_m = []
        for page in range(1,2):

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


df.drop(['순위변화', '아이돌 평점주기'], axis='columns', inplace=True)
display(df)

df.to_excel('test.xlsx', sheet_name = 'Sheet1')