import time
from selenium.webdriver import Chrome
import pandas as pd
from IPython.display import display
import numpy as np

# 참고사이트
# https://dev.to/lewiskori/beginner-s-guide-to-web-scraping-with-python-s-selenium-3fl9


webdriver = "chromedriver.exe"



driver = Chrome(webdriver)
total_y =[]
for month in range(1,3):
    total_m = []
    for page in range(1,6):

        url = "https://www.idol-chart.com/ranking/month/?sm=2018"+str(month).rjust(2, '0')+"&page=" +str(page)

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
        result[i].append("2018"+str(month).rjust(2, '0'))
    total_y.append(result)
driver.close()

total_y = np.array(total_y)
print(total_y)
# total_y = total_y.reshape(total_y.shape[0] * total_y.shape[1], total_y.shape[2])
# df = pd.DataFrame(total_y, columns=['순위', '아이돌', '음원/음반', '유튜브', '전문가/평점랭킹', '방송/포털/소셜', '총점', '순위변화', '아이돌 평점주기', '날짜'])
# df.drop(['순위변화', '아이돌 평점주기'], axis='columns', inplace=True)
# display(df)
