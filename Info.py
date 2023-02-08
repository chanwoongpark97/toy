import requests # requests 라이브러리 설치 필요
from bs4 import BeautifulSoup

r = requests.get('http://spartacodingclub.shop/sparta_api/seoulair')
rjson = r.json()

gus = rjson['RealtimeCityAir']['row']

for gu in gus:
	if gu['IDEX_MVL'] < 35:
		print (gu['MSRSTE_NM'], gu['IDEX_MVL'])

# 설치한 라이브러리
# requests : API 데이터 추출용도(위 구문이 예시)
# bs4 : 웹 크롤링을 위한 BeautifulSoup
# pymongo : mongoDB연결
# dnspython : pymongo패키지 동작용
# flask : 웹 서버 프레임워크
# certifi : 보안문제 해결용

# 크롤링 데이터 (인터파크 뮤지컬 정보)
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get('http://ticket.interpark.com/contents/Ranking/RankList?pKind=01011&pCate=&pType=W&pDate=20230206',
#                     headers=headers)
# soup = BeautifulSoup(data.text, 'html.parser')
#
# musicals = soup.select('body > div.rankingDetailBody > div')
# for musical_cul in musicals:
#     title = musical_cul.select_one('td.prds > div.prdInfo > a > b')
#     if title is not None:  # 제목에 None값이 있으면 출력이 정상적으로 안됨
#         name = title.text
#         image = musical_cul.select_one('td.prds > a > img')['src']  # 이미지가 alt , src가 잡히는데 alt는 NO_image여서 src의 데이터를 가져옴
#         content = musical_cul.select_one('td.prdDuration').text.strip()  # 공백제거를 위한 .strip()내장함수 사용
#         print(name, image, content)
#         doc = {   #계속 데이터가 삽입되는 것을 방지하고자 주석처리.
#             'category': '뮤지컬',
#             'image': image,
#             'name': name,
#             'content': content,
#         }
#         db.musical.insert_one(doc)  #데이터 삽입.

# 크롤링 데이터 (지니뮤직 음원 정보)
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get('https://www.genie.co.kr/chart/top200?ditc=M&rtm=N&ymd=20210701', headers=headers)
# soup = BeautifulSoup(data.text, 'html.parser')
# genies = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
#
# for genie in genies:
#     music = genie.select_one('td.number').text[0:2]
#     image = genie.select_one('td:nth-child(3) > a > img')['src']
#     name = genie.select_one('td.info > a.title.ellipsis').text.strip()
#     artist = genie.select_one('td.info > a.artist.ellipsis').text
#     content = genie.select_one('td.info > a.albumtitle.ellipsis').text
#
#     doc = {
#                   'category': 'category',
#                   'image': image,
#                   'name': name,
#                   'content': content,
#                   'artist': artist,
#               }
    # db.music.insert_one(doc)

# 크롤링 데이터 (다음 영화 정보)
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get('https://movie.daum.net/ranking/boxoffice/weekly',headers=headers)
# soup = BeautifulSoup(data.text, 'html.parser')
# movies = soup.select('#mainContent > div > div.box_boxoffice > ol > li')
#
# for movie in movies:
#     a = movie.select_one('div > div.thumb_cont > strong > a')
#     b = movie.select_one('div > div.thumb_cont > span > span:nth-child(1) > span')
#     c = movie.select_one('div > div.thumb_item > div.poster_movie > img')
#     if a is not None:
#         category = '영화' # 한 종류의 카테고리를 나타낼때는 변수형으로
#         title = a.text # 텍스트 추출
#         date = b.text # 텍스트 추출
#         image = c.get('src') # 태그의 속성값을 추출할 때에는 get메소드를 이용한다. [element.get('속성값')]
#         print(category, image, title, date)
#         # doc = {
#         #           'category': category,
#         #           'image': image,
#         #           'name': title,
#         #           'date': date
#         #       }
#         # db.movie.insert_one(doc)

