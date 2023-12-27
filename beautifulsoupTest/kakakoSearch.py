import requests
from bs4 import BeautifulSoup
import csv

# 검색어 및 기간 설정
search_query = "카카오뱅크"
start_date = "2021.12.16."
end_date = "2023.12.26."
base_url = "https://kin.naver.com/search/list.nhn"
i = 1
# 수집된 데이터를 저장할 리스트
data = []

# 페이지별 크롤링
for page in range(1, 3001):
    url = f"{base_url}?sort=none&query={search_query}&period={start_date}|{end_date}&section=kin&page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 각 질문의 상세 페이지 링크 추출 및 절대 URL 변환
    for link in soup.select("._searchListTitleAnchor"):
        detail_url = link.get('href')

        detail_response = requests.get(detail_url)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

        # 제목과 내용 추출
        title = detail_soup.select_one(".title").text.strip()
        content_element = detail_soup.select_one(".c-heading__content")
        content = content_element.text.strip() if content_element else "내용없음"

        # 데이터 리스트에 추가
        data.append([title, content])
        i += 1
        print(i)

# CSV 파일로 저장
with open('kakao_bank_data.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Content'])  # 컬럼명 작성
    writer.writerows(data)  # 데이터 작성
