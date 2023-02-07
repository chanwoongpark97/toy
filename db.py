import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@Cluster0.zhropba.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.daum.net/ranking/boxoffice/weekly',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')

#카피 셀렉터로 영화 제목 구성 조사
#mainContent > div > div.box_boxoffice > ol > li:nth-child(1) > div > div.thumb_cont > strong > a
#mainContent > div > div.box_boxoffice > ol > li:nth-child(2) > div > div.thumb_cont > strong > a
#카피 셀렉터로 개봉 날짜 구성 조사
#mainContent > div > div.box_boxoffice > ol > li:nth-child(1) > div > div.thumb_cont > span > span:nth-child(1) > span
#카피 셀렉터로 영화 포스터 이미지 구성 조사
#mainContent > div > div.box_boxoffice > ol > li:nth-child(1) > div > div.thumb_item > div.poster_movie > img
#select를 이용해서, tr들을 불러오기

movies = soup.select('#mainContent > div > div.box_boxoffice > ol > li')

for movie in movies:
    a = movie.select_one('div > div.thumb_cont > strong > a')
    b = movie.select_one('div > div.thumb_cont > span > span:nth-child(1) > span')
    c = movie.select_one('div > div.thumb_item > div.poster_movie > img')
    if a is not None:
        category = '영화' # 한 종류의 카테고리를 나타낼때는 변수형으로
        title = a.text # 텍스트 추출
        date = b.text # 텍스트 추출
        image = c.get('src') # 태그의 속성값을 추출할 때에는 get메소드를 이용한다. [element.get('속성값')]
        print(category, image, title, date)
        # doc = {
        #           'category': category,
        #           'image': image,
        #           'name': title,
        #           'date': date
        #       }
        # db.culture.insert_one(doc)