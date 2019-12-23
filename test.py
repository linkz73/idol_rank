#
'''
import requests
from bs4 import BeautifulSoup

import time



headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip",
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}
url = "https://www.idol-chart.com/ranking/month/?sm="
result = requests.get(url=url, headers=headers)

bs_obj = BeautifulSoup(result.text, "html.parser")
time.sleep(3)
print(bs_obj)
'''

import time
from selenium.webdriver import Chrome
import pandas as pd

webdriver = "c:\python\chromedriver.exe"

driver = Chrome(webdriver)


# url = "https://www.idol-chart.com/"
url = "https://www.idol-chart.com/ranking/month/?sm=201911"

# url = "http://quotes.toscrape.com/js/page/" + str(page) + "/"

driver.get(url)
time.sleep(3)
# items = driver.find_elements_by_class_name("section")
items = driver.find_elements_by_class_name("layout-bbs")
trs = items.find_elements_by_tag_name("tr")
# df = pd.DataFrame(items,columns=['순위','아이돌'])
total = list()
for tr in trs:
    td = tr.find_element_by_tag_name('td').text
    print(td)
    # total.append(new)
# df = pd.DataFrame(items)
# print(df)
# for ii in items:
#     print(ii.text)

driver.close()
