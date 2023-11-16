from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime
from bs4 import BeautifulSoup



url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head=0&page=1'

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

category = ['Normal', 'News', 'Review', 'Tip', 'Mod']


def func(t):
    df_titles = pd.DataFrame()
    titles = []
    pages = [1]
    category_list = [0, 330, 20, 340, 350]
    url_list=[]


    url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page=1'.format(category_list[t])
    # print(url)
    for k in range(1, pages[0]+1):
        G_url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page={}'.format(category_list[t], k)
        driver.get(G_url)
        time.sleep(0.5)  # 페이지를 바꿀 시간을 줘야한다 없으면 에러가 발생할 수 있음.
        for i in range(2, 47):
            try:
                title_element = driver.find_element('xpath', f'//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[{i}]/td[3]/a[1]')
                title = title_element.text
                title_element.click()
                # title = driver.find_element('xpath',
                #                             '//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[{}]/td[3]/a[1]'.format(i)).click()
                time.sleep(0.5)
                # title = re.compile('').sub('', title))
                current_url = driver.current_url
                url_list.append(current_url)

                # titles.append(title)
                # 다시 목록 페이지로 돌아가기
                driver.back()
                time.sleep(0.5)  # 페이지 이동을 기다립니다.
            except Exception as e:
                print(f"Error {i}: {str(e)}")

    return url_list

url_list = func(0)

df_test = pd.DataFrame()

for url in url_list:
    print(url)
    df_test.to_csv('./linked.csv',index=False)

