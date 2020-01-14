import bs4
from selenium import webdriver
from datetime import datetime
import os
import urllib.request
import re


options = webdriver.ChromeOptions()
options.add_argument('headless') # 팝업창 안띄우는 속성
# options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome('chromedriver', chrome_options=options)
# driver.get('https://blog.naver.com/kmw123m/221364161554') #se_component_wrap sect_dsc __se_component_area 속성 블로그
# driver.get('https://blog.naver.com/skcmi/221436159512/') #se-main-container 속성 블로그
# driver.implicitly_wait(3)
# driver.switch_to.frame('mainFrame')
# html = driver.page_source
#
# bs_obj = bs4.BeautifulSoup(html, "html.parser")

def Naver(url):
    driver.get(url)  # se-main-container 속성 블로그
    driver.implicitly_wait(3)
    driver.switch_to.frame('mainFrame')
    html = driver.page_source

    bs_obj = bs4.BeautifulSoup(html, "lxml")
    ul = bs_obj.find("div", {"class":"se-main-container"})

    if ul!=None:
        ul = bs_obj.find("div", {"class": "se-main-container"})  # 본문 영역 가져오기

        # lis= str(ul.findAll("p"))
        lis = ul.findAll("p")  # 문장이 있는 p 태그 추출
        lis2 = ul.findAll("img", {"class": "se-sticker-image"})  # 이모티콘 추출
        image = ul.findAll("img", {"class": "se-image-resource"})  # 이미지 추출
        canvas = ul.findAll("div", {"class": "se-component se-video se-l-default"})  # 동영상 추출

        list = []  # 문자를 넣어주기 위한 리스트

        for li in lis:  # \u200b 제거후 텍스트 추출
            if li.text != '\u200b':
                list.append(li.text)  # 빈 리스트에 li의 텍스트를 반복문으로 이어 붙이기

        for li2 in lis2:  # 이모티콘 개수
            str(lis2).count("img")

        for li3 in image:  # 이미지 개수
            # print(li3)
            str(image).count("img")

        for li4 in canvas:  # 동영상 개수
            str(canvas).count("se-component se-video se-l-default")

        print("이모티콘 개수 : ", str(lis2).count("img"), "개")
        print("이미지 개수 : ", str(image).count("img"), "개")
        print("동영상 개수 : ", str(canvas).count("se-component se-video se-l-default"), "개")
        print(list)

    else:
        ul = bs_obj.find("div", {"class":"se_component_wrap sect_dsc __se_component_area"}) # 본문 영역 가져오기
        image = ul.findAll("div", {"class": "se_component se_image default"}) #이미지 추출
        lis2 = ul.findAll("img", {"class": "__se_img_el"}) #이모티콘 추출
        canvas = ul.findAll("div", {"class": "_video_thumb"}) # 동영상 추출

        lis= ul.findAll("p")
        list = [] #문자를 넣어주기 위한 리스트

        for li in lis:  # \u200b 제거후 텍스트 추출

            list.append(str(li.text.replace("\xa0", ""))) #빈 리스트에 li의 텍스트를 반복문으로 이어 붙이기


        for li2 in image: #이미지 개수
            str(image).count("imgId")

        for li4 in canvas: #동영상 개수
            str(canvas).count("_video_thumb")


        for li2 in lis2: #이모티콘 개수
            str(lis2).count("img")

        print("이미지 개수 : ", str(image).count("imgId"), "개")
        print("동영상 개수 : ",str(canvas).count("_video_thumb"),"개")
        print("이모티콘 개수 : ", str(lis2).count("스티커 이미지"), "개")
        print(list)


# Naver()
start_time = datetime.now()
url1 = 'https://blog.naver.com/skcmi/221436159512/'
Naver(url1)
url2 = 'https://blog.naver.com/kmw123m/221364161554'
Naver(url2)
url3 = 'https://blog.naver.com/skcmi/221767496118'
Naver(url3)

print("time : ", datetime.now() - start_time)

