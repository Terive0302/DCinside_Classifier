from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


def func(category_num, page_num):
    pages = [page_num]
    category_list = [0, 330, 20, 340, 350]
    url_list=[]

    for k in range(1, pages[0]+1):
        G_url = ('https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head={}&page={}'
                 .format(category_list[category_num], k))
        driver.get(G_url)
        time.sleep(0.5)  # 페이지를 바꿀 시간을 줘야한다 없으면 에러가 발생할 수 있음.
        for i in range(2,47):
            try:
                title_element = driver.find_element('xpath', f'//*[@id="container"]'
                                                             f'/section[1]/article[2]/div[2]/table/tbody/tr[{i}]/td[3]/a[1]')
                title_element.click()
                time.sleep(1)
                current_url = driver.current_url
                url_list.append(current_url)

                driver.back()
                time.sleep(1)  # 페이지 이동을 기다립니다.
            except Exception as e:
                print(f"Error {i}: {str(e)}")

            with open('url.csv', 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)

                # 리스트의 각 항목을 CSV 파일에 작성
                for url in url_list:
                    csv_writer.writerow([url])

    return 0

if __name__ == '__main__':
    url = 'https://gall.dcinside.com/mgallery/board/lists/?id=mouse&sort_type=N&search_head=0&page=1'

    options = ChromeOptions()
    user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/61.0.3163.100 Safari/537.36")
    options.add_argument('user-agent=' + user_agent)
    options.add_argument("lang=ko_KR")

    # 크롬 드라이버 최신 버전 설정
    service = ChromeService(executable_path=ChromeDriverManager().install())

    # chrome driver
    driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

    category = ['Normal', 'News', 'Review', 'Tip', 'Mod']
    url_list1 = func(0, 1)

func(0,2)



