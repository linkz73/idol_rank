import time
from selenium.webdriver import Chrome
import pandas as pd

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
    tr = item.find_element_by_tag_name('tr').text
    print(tr)
    # total.append(new)
# df = pd.DataFrame(items)
# print(df)

# driver.close()
