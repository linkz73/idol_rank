import time
from selenium.webdriver import Chrome
import pandas as pd

# 참고사이트
# https://dev.to/lewiskori/beginner-s-guide-to-web-scraping-with-python-s-selenium-3fl9


webdriver = "chromedriver.exe"

driver = Chrome(webdriver)

url = "https://www.idol-chart.com/ranking/month/?sm=201911"

# url = "http://quotes.toscrape.com/js/page/" + str(page) + "/"

driver.get(url)
time.sleep(3)
# items = driver.find_elements_by_class_name("section")
items = driver.find_elements_by_class_name("layout-bbs")
# df = pd.DataFrame(items,columns=['순위','아이돌'])
total = list()
for item in items:
    trs = item.find_element_by_tag_name('tr').text
    print(trs)
    # total.append(new)
# df = pd.DataFrame(items)
# print(df)

# driver.close()
