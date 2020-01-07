import time
from IPython.display import display
from selenium.webdriver import Chrome
import pandas as pd
import numpy as np

# 참고사이트
# https://dev.to/lewiskori/beginner-s-guide-to-web-scraping-with-python-s-selenium-3fl9
def from_iterable(iterables):
    # chain.from_iterable(['ABC', 'DEF']) --> ['A', 'B', 'C', 'D', 'E', 'F']
    for it in iterables:
        for element in it:
            yield element

webdriver = "chromedriver.exe"

driver = Chrome(webdriver)

url = "https://www.idol-chart.com/ranking/month/?sm=201801"

# url = "http://quotes.toscrape.com/js/page/" + str(page) + "/"

driver.get(url)
time.sleep(3)
# items = driver.find_elements_by_class_name("section")
items = driver.find_elements_by_tag_name("td")
total=[]

for item in items:
    split_item = []
    split_item.append(item.text)
    result = list(map(lambda x: x.replace(',',"").replace(' ',''),split_item))
    total.append(result)
    # print(result)
    # total.append(result)
    # sub = []
    # for i in split_item:
    #     sub.append(i.replace(",",""))
    # total.append(sub)
# del total[0]
# 이중 리스트의 모양을 flatten 하게 하는 함수
total = sum(total,[])
# 일정한 크기로 나눠주는 함수
n = 9
result = [total[i * n:(i + 1) * n] for i in range((len(total) + n - 1) // n )]
# print(result)
for i in range(len(result)):
    result[i].append("201801")
driver.close()

df = pd.DataFrame(result, columns=['순위','아이돌','음원/음반','유튜브','전문가/평점랭킹','방송/포털/소셜','총점','순위변화','아이돌 평점주기','날짜'])
df.drop(['순위변화','아이돌 평점주기'], axis='columns', inplace=True)
display(df)
'''
for item in items:
    item = str.maketrans(',','')
    split_item = item.text.split()
    total.append(split_item)
del total[0]


df = pd.DataFrame(data=np.array(total)) columns=['순위','아이돌', '음원/음반', '유튜브', '전문가/평정랭킹', '방송/포털/소셜', '총점', '순위변화', '아이돌 평점주기'])
display(pd.DataFrame(df))
# df = pd.DataFrame(items)
# print(df)

driver.close()
'''