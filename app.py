from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.zhropba.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://ticket.interpark.com/contents/Ranking/RankList?pKind=01011&pCate=&pType=W&pDate=20230206',
                    headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# 크롤링 데이터 (인터파크 뮤지컬 정보)
musicals = soup.select('body > div.rankingDetailBody > div')
for musical_cul in musicals:
    title = musical_cul.select_one('td.prds > div.prdInfo > a > b')
    if title is not None:  # 제목에 None값이 있으면 출력이 정상적으로 안됨
        name = title.text
        image = musical_cul.select_one('td.prds > a > img')['src']  # 이미지가 alt , src가 잡히는데 alt는 NO_image여서 src의 데이터를 가져옴
        content = musical_cul.select_one('td.prdDuration').text.strip()  # 공백제거를 위한 .strip()내장함수 사용
        # print(name, image, content)
        # doc = {   #계속 데이터가 삽입되는 것을 방지하고자 주석처리.
        #     'category': '뮤지컬',
        #     'image': image,
        #     'name': name,
        #     'content': content,
        # }
        # db.musical.insert_one(doc)  #데이터 삽입.

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=M&rtm=N&ymd=20210701',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

genies = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
for genie in genies :
    # music = genie.select_one('td.number').text[0:2]
    image = genie.select_one('td:nth-child(3) > a > img')['src']
    name = genie.select_one('td.info > a.title.ellipsis').text.strip()
    content = genie.select_one('td.info > a.albumtitle.ellipsis').text


    # doc = {
    #               'category': 'category',
    #               'image': image,
    #               'name': name,
    #               'contet': content
    #           }
    # db.music.insert_one(doc)

# 송 수신
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/movie_List')
def movie_List():
    return render_template('movie_List.html')

@app.route('/book_List')
def book_List():
    return render_template('book_List.html')

@app.route('/music_List')
def music_List():
    return render_template('music_List.html')

@app.route('/musical_List')
def musical_List():
    return render_template('musical_List.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/board')
def board():
    return render_template('board.html')

@app.route('/join', methods=['GET'])
def test_get():
    title_receive = request.args.get('title_give')
    print(title_receive)
    return jsonify({'result': 'success', 'msg': '이 요청은 GET!'})

@app.route('/join', methods=['POST'])
def test_post():
    title_receive = request.form['title_give']
    print(title_receive)
    return jsonify({'result': 'success', 'msg': '회원 가입 완료.'})

#board
@app.route("/board", methods=["POST"])
def board_post():
    writer_receive = request.form["writer_give"]
    comment_receive = request.form["comment_give"]
    date_receive = request.form["date_give"]

    doc = {
        'writer': writer_receive,
        'comment': comment_receive,
        'date': date_receive
    }

    db.board.insert_one(doc)
    return jsonify({'msg':'한줄평 작성 완료!'})

@app.route("/boards", methods=["GET"])
def board_get():
    board_list = list(db.board.find({},{'_id':False}))
    return jsonify({'board_list':board_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
