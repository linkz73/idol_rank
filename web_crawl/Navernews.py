import requests
from urllib.parse import urlparse
import re
from newspaper import Article
from gensim.summarization.summarizer import summarize
from konlpy.tag import Kkma
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from wordcloud import ImageColorGenerator
import nltk
import matplotlib.pyplot as plt

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# path = os.path.join(BASE_DIR, 'web_crawl/sub_word.txt')
#
# with open(path, 'rt', encoding='ANSI') as data:
#     words = data.readlines()
#     words = list(map(lambda s: s.rstrip(), words))

def get_api_result(keyword, display, start):
    url = "https://openapi.naver.com/v1/search/news?query=" + keyword +"&display=" +str(display)\
          +"&start=" +str(start)+ "&sort=sim"     # 유사성을 기준으로
    result = requests.get(urlparse(url).geturl(),
                          headers={"X-Naver-Client-Id": "GQKArseCDOh1t1AMHtxQ",
                                   "X-Naver-Client-Secret": "yf6tWSa_Zl"})
    return result.json()

def call_and_print(keyword, page, page_info_list):
    json_obj = get_api_result(keyword, 10, page)
    for item in json_obj['items']:
        title = item['title'].replace("<b>", "").replace("</b>", "").replace("&lt;", "").replace("&gt;", "").replace("&quot;","")
        link = item['originallink']
        result = (title, link)
        page_info_list.append(result)

def make_content(url_list, news_content_list,  content_summarize_list, title_list):
    for url in url_list:
        try:
            kkma = Kkma()
            news =Article(url, language = 'ko')
            news.download()
            news.parse()
            title_list.append(news.title)
            news.text = kkma.sentences(news.text)
            news.text = " ".join(news.text)
            news_content_list.append(news.text)
            # print(news.text)
            # print(type(news.text))
            summary_content = summarize(news.text, word_count=100, ratio= 0.5)
            if summary_content != None:
                content_summarize_list.append(summary_content)
            else:
                content_summarize_list.append("기사의 내용이 없습니다.")
        except Exception as e:
            print("exceptions is ", e)
            pass

def wordcloud(news_content_list, page_info_list, img_url):
    for i in range(len(news_content_list)):
        try:
            kkma = Kkma()
            tokens_ko = kkma.nouns(news_content_list[i])
            ko = nltk.Text(tokens_ko, name=page_info_list[i][0])
            data = ko.vocab().most_common(100)

            tmp_data = dict(data)

            korea_coloring = np.array(Image.open("C:\Study\project_idol\web_crawl\/Korea.png"))
            image_colors = ImageColorGenerator(korea_coloring)
            wordcloud= WordCloud(font_path = 'c:\\windows\\fonts\\NanumGothic.ttf',
                                 relative_scaling=0.1,
                                 mask=korea_coloring,
                                 background_color='black',
                                 min_font_size=4,
                                 max_font_size=40,
                                 ).generate_from_frequencies(tmp_data)
            plt.figure(figsize=(12,12))
            plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
            title = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', page_info_list[i][1])
            wordcloud.to_file("C:\Study\project_idol\static\wordcloud\/" + title +".png")
            plt.axis("off")
            url = "wordcloud\/" + title +".png"
            url = re.sub('/','',url)
            img_url.append(url)
            # plt.show()
        except Exception as e:
            print("exceptions is ", e)
            pass
# input = input('검색할 단어 > ')
# page_info_list = []
# url_list = []
# title_list = []
# news_content_list = []
# img_url = []
# content_summarize_list = []
# call_and_print(input, 1, page_info_list)
# for i in range(len(page_info_list)):
#     url_list.append(page_info_list[i][1])
# print(url_list)
#
# make_content(url_list, news_content_list, content_summarize_list, title_list)
# wordcloud(news_content_list, page_info_list, img_url)
# print(img_url)