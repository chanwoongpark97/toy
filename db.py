import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.zhropba.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://ticket.interpark.com/contents/Ranking/RankList?pKind=01011&pCate=&pType=W&pDate=20230206',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# 크롤링 데이터 (인터파크 뮤지컬 정보)
musicals = soup.select('body > div.rankingDetailBody > div')
for musical in musicals:
    title = musical.select_one('td.prds > div.prdInfo > a > b')
    if title is not None:   #제목에 None값이 있으면 출력이 정상적으로 안됨
        name = title.text
        image = musical.select_one('td.prds > a > img')['src']  #이미지가 alt , src가 잡히는데 alt는 NO_image여서 src의 데이터를 가져옴
        date = musical.select_one('td.prdDuration').text.strip()    #공백제거를 위한 .strip()내장함수 사용
        # doc = {   #계속 데이터가 삽입되는 것을 방지하고자 주석처리.
        #     'category': '뮤지컬',
        #     'image': image,
        #     'name': name,
        #     'date': date,
        # }
        # db.culture.insert_one(doc)  #데이터 삽입.

musical_list = list(db.culture.find({},{'_id':False}))
for musical in musical_list:
    print(musical)

# db연결 세팅 끝.
# certifi가 없으면 db에 데이터 저장이 안됨.
