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


@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movie.find({}, {'_id': False}))
    return jsonify({'movies':movie_list})

@app.route("/music", methods=["GET"])
def music_get():
    music_list = list(db.music.find({}, {'_id': False}))
    return jsonify({'musics':music_list})

# 송 수신
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/movie_List')
def movie_List():
    return render_template('movie_List.html')

@app.route('/book_List')
def book_List():
    return render_template('book_List.html')

@app.route('/music_List')
def music_List():
    return render_template('music_List.html')

@app.route('/books')
def books():
    return render_template('book_List.html')

@app.route('/musical_List')
def musical_List():
    return render_template('musical_List.html')

@app.route("/musicalInfo", methods=["GET"])
def musical_get():
    musical_info = list(db.musical.find({}, {'_id': False}))
    return jsonify({'musicalInfo':musical_info})

@app.route("/musicalsearch_list", methods=["GET"])
def musicalsearch_list_get():
    musical_list = list(db.musical.find({}, {'_id': False}))
    return jsonify({'musicals': musical_list})

@app.route('/login')
def login():
    return render_template('login.html')

# 추가
@app.route("/loginchk", methods=["GET"])
def login_get():
    user_list = list(db.member.find({}, {'_id': False}))
    return jsonify({'user_list':user_list})

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

@app.route("/join", methods=["POST"])
def join_post():
    userId_receive = request.form['userId_give']
    userPw_receive = request.form['userPw_give']
    userName_receive = request.form['userName_give']
    userPhone_receive = request.form['userPhone_give']

    userId_list = list(db.member.find({}, {'_id': False}))

    if userId_receive == '' or userPw_receive == '' or userName_receive == '' or userPhone_receive == '':
        return jsonify({'msg': '정보를 입력하세요.'})
    elif userId_receive != '' and userPw_receive != '' and userName_receive != '' and userPhone_receive != '':
        doc = {
            'userId': userId_receive,
            'userPw': userPw_receive,
            'userName': userName_receive,
            'userPhone': userPhone_receive,
        }
        db.member.insert_one(doc)

        userId_str = str(userId_receive)
        for i in userId_list:
            if i['userId'] == userId_str:
                return jsonify({'msg': '중복된 id 입니다.'})
        return jsonify({'msg': '회원가입 완료.'})

@app.route("/book", methods=["GET"])
def book_get():
    book_list = list(db.books.find({}, {'_id': False}))
    return jsonify({'books': book_list})

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

@app.route("/search_list", methods=["GET"])
def search_get():
    book_list = list(db.books.find({}, {'_id': False}))
    return jsonify({'books': book_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
