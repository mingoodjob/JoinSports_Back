from datetime import datetime, timedelta
import hashlib
import json
from bson import ObjectId
import jwt
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from pymongo import MongoClient
import certifi

SECRET_KEY = 'turtle'
                       
client = MongoClient('mongodb+srv://seonyoung:seonyoung@cluster0.fjbmmzj.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.joinsports

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/")
def hello_world():
    return jsonify({'message': 'success'})



@app.route("/join", methods=["POST"])
def join():
    
    email = request.form['email']
    nick = request.form['nick']
    pwd = request.form['pwd']
    image = request.files['filegive']
    print(email, nick, pwd, image.filename)
    image.save(f'./image/{image.filename}')


    # 비밀번호 해싱
    hashed_password = hashlib.sha256(pwd.encode('utf-8')).hexdigest()

    
    doc = {
        'email': email, 
        'nick' : nick,
        'password': hashed_password,
        'pr_photo' : f'{image.filename}'
       
    }


    db.users.insert_one(doc)

    return jsonify({"status": "success"})



#이메일 중복 확인
@app.route("/join/check_email", methods=["POST"])
def check_email():
    email_receive = request.form['email_give']
    is_exists = db.users.find_one({'email': email_receive})
    if is_exists:
        return jsonify({'result': 'fail'})
    return jsonify({'result': 'success'})

@app.route("/join/check_nick", methods=["POST"])
def check_nick():
    nick_receive = request.form['nick_give']
    is_exists = db.users.find_one({'nick': nick_receive})
    if is_exists:
        return jsonify({'result': 'fail'})
    return jsonify({'result': 'success'})




@app.route("/login", methods=["POST"])
def login():
    print(request)
    data = json.loads(request.data)
    print(data)
    #로그인에서 데이터는 request data를 불러온다.

    email = data.get("email")
    password = data.get("password")
    #email과 password는 data에서 각각 가져오는데,
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
    #해싱된_비밀번호는 = 이렇게 해싱처리 해준다.
    print(hashed_pw)

    result = db.users.find_one({
        'email': email,
        'password': hashed_pw
    })
    #result는 db에서 email과 hashed_pw를 찾아온 값들로 정의한다.

    print(result)

    if result is None:
        return jsonify({"message": "아이디나 비밀번호가 옳지 않습니다."}), 401
        #result에 값이 없으면(아이디, 패스워드가 비워져있으면) 로그인에 실패했기 때문에 401신호 

    payload = {
        'id': str(result["_id"]),
        #(result의 _id = mongodb에서 만들어준 primary key)를 string화.string을 하지 않으면 object id만 출력되기 때문에
        'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    #jwt 인코딩
    print(token)
    #토큰 안에 들어갈 내용
    #토큰 출력한 걸 google jwt검색 후 입력하고 secret key입력하면 정보가 잘 나오는지 확인.

    return jsonify({"message": "로그인 성공!", "result":"success", "token": token})

    # massage와 token돌려주기


    # @app.route("/getuserinfo", methods=["GET"])
    # #user의 이름 가져오기
    # def get_user_info():
    #     token = request.headers.get("Authorization")
    #     #공통적으로 실어서 보내는 값은 header에 실어서 보내게 된다.

    #     if not token:
    #         return jsonify({"message": "no token"}), 402

    #     user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    #     result = db.users.find_one({
    #         '_id': ObjectId(user["id"])
    #     })

    #     return jsonify({"message": "success"})


if __name__ == '__main__' :
    app.run('0.0.0.0', port=5001, debug=True)
    