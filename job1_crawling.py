# Dcinside 마우스 마이너 갤러리의 'Normal', 'News', 'Review', 'Tip', 'Mod'
# 5개의 탭에 접근해 각 페이지 의 제목과, 카테고리 를 저장 하는 코드 입니다.

# test_YH.py 의 코드를 기반 으로 수정 했습니다.
# 제목만 긁어오는게 목적이기 때문에 각 글의 페이지에 직접 접근 하지 않고
# xpath 를 이용하여 text만 가져왔습니다.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time


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

titles = []
pages = [10]
# 페이지 지정 1~ 10 까지 [10] 넣으면 아래 for문 에서  10페이지까지 긁어옵니다.
category_list = [0, 330, 20, 340, 350]

# 빈 DataFrame 생성 컬럼은 'titles', 'category'
df_all = pd.DataFrame(columns=['titles', 'category'])

for ll in range(len(category)):
    url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page=1'.format(category_list[ll])
    # print(url)
    for k in range(1, pages[0]+1):  # pages[0]+1 인덱스 접근
        G_url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page={}'.format(category_list[ll], k)
        driver.get(G_url)
        time.sleep(0.5)  # 페이지를 바꿀 시간을 줘야한다 없으면 에러가 발생할 수 있음.
        for i in range(2, 47): # 1페이지 안의 글 갯수 기본값 47/ 테스트를 위해 5로 설정..
            try:
                title_element = driver.find_element('xpath', f'//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[{i}]/td[3]/a[1]')
                # 제목의 xpath
                title = title_element.text
                # title 변수에 .text를 사용해서 저장.
                title = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', title)
                # 제목을 가~힣, a~z, A~z 까지의 문자만 남기고 나머지 문자는 ' ' 공백으로 채운다.
                titles.append(title)
                # titles 리스트에  title 을 추가한다.
                time.sleep(0.1)
                # 대기!

                df_temp = pd.DataFrame({'titles': [title], 'category': [category[ll]]})
                df_all = pd.concat([df_all, df_temp], ignore_index=True)

            except Exception as e:
                print(f"Error {i}: {str(e)}")
            if i == 46:
                # 페이지의 글 목록이 1번째가 공지글이라 2~ 46까지 45개..
                # 마지막 글을 i가 46이면 긁어 올때이다.

                df_all.to_csv('./crawling_data/DC_v1_{}_{}.csv'.format(category[ll], k), index=False)
                # 페이지의 글이 45번쨰까지 긁어지면 경로에 카테고리_페이지 형식으로 저장.

df_all.to_csv('./crawling_data/DC_v1.csv', index=False)
# 모든 작업이 끝난후 './crawling_data/DC_v1.csv' 경로에 모든 데이터 를 저장 합니다.
