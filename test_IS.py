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



titles = []
texts = []
pages = [1]
# 페이지 지정 1~ 10 까지 [10] 넣으면 아래 for문 에서  10페이지까지 긁어옵니다.
category_list = [0, 330, 20, 340, 350]
category = ['Normal', 'News', 'Review', 'Tip', 'Mod']

url_list=[]

for ll in range(len(category_list)):
    # for i in category_list:

    url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page=1'.format(category_list[ll])
    for k in range(1, pages[0]+1):  # pages[0]+1 인덱스 접근
        G_url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page={}'.format(category_list[ll], k)
        driver.get(G_url)
        time.sleep(0.5)  # 페이지를 바꿀 시간을 줘야한다 없으면 에러가 발생할 수 있음.
        for i in range(2, 5): # 1페이지 안의 글 갯수 기본값 47/ 테스트를 위해 5로 설정..
            try:
                title_element = driver.find_element('xpath', f'//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[{i}]/td[3]/a[1]')
                title = title_element.text
                title = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', title)
                titles.append(title)
                # titles 에 제목 <title> 텍스트 저장
                title_element.click()
                # 제목의 요소 클릭 클릭만 쭈르륵 하고 다음 카테고리로  계속 넘어감 딜레이를 넣으면 여기에?
                time.sleep(0.5)
                # 대기!
                text = driver.find_element('xpath','//*[@id="container"]/section/article[2]/div[1]/div/div[1]/div[1]').text
                text = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', text)
                texts.append(text)

                driver.back()
                time.sleep(0.5)  # 페이지 이동을 기다립니다.
            except Exception as e:
                print(f"Error {i}: {str(e)}")
    df_section_title = pd.DataFrame(titles, columns=['titles'])
    # titles 컬럼을 만들고 타이틀 대입.

    df_section_title['category'] = category[i]
    # category = ['Normal', 'News', 'Review', 'Tip', 'Mod']
    df_section_title['text'] = texts
    df_section_title.to_csv('../crawling_data/DC_v1.csv', index=False)
# for ii in range(2):
#     df_section_title = pd.DataFrame(titles, columns=['titles'])
#     # titles 컬럼을 만들고 타이틀 대입.
#     df_section_title['category'] = category[ii]
#     df_section_title['text'] = texts
#     df_section_title.to_csv('../crawling_data/DC_v1.csv', index=False)
# print(titles)
# for i in range(27):
#     print(titles[i])
#     print(texts[i])
#     print('\n\n\n')
#




# print(texts)

   # list 에 url 목록이 들어가있음. 'url주소','url주소'
# for url in url_list:
#     print(url)
#
# df_url = pd.DataFrame()
# df_url.to_csv('../Dc_url.csv', index=False)  # index=False를 지정하면 인덱스 열을 저장하지 않습니다.
#