from datetime import datetime, timedelta
# from functools import wraps
from bson import ObjectId
from flask import Flask, abort, jsonify, request, Response
from flask_cors import CORS
from pymongo import MongoClient
import hashlib,certifi,jwt,json
import maincrud,model
client = MongoClient('mongodb+srv://test:sparta@cluster0.avef3.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.joinsports
SECRET_KEY = 'turtle'

# model.model_load()

# def authorize(f):  # 데코레이션 함수 정의 (f)로 인자를 전달 받을 수 있도록함
#     def decorated_function():  # 반복해야할 함수 정의
#         if not 'Authorization' in request.headers:
#             abort(401)
#         token = request.headers['Authorization']
#         try:
#             user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#         except:
#             abort(401)
#         return f(user)  # f인자에 변수 user를 담음
#     return decorated_function

app = Flask(__name__)
cors = CORS(app, resources={
            r'*': {'origins': ['http://127.0.0.1:5001', 'http://127.0.0.1:5500']}})

@app.route("/")
def Home():
    return jsonify({'result': 'happy'})

@app.route("/join", methods=["POST"])
def join():
    
    email = request.form['email']
    nick = request.form['nick']
    pwd = request.form['pwd']
    image = request.files['filegive']
    image.save(f'static/img/{image.filename}')
    # category = '1'
    imagefile = maincrud.img_save(f'static/img/{image.filename}')
    category = model.result_ct(f'{image.filename}')
    # imagefile = f'{image.filename}'

    # 비밀번호 해싱
    hashed_password = hashlib.sha256(pwd.encode('utf-8')).hexdigest()

    maincrud.user_save(email,hashed_password,nick,imagefile,category)

    return jsonify({"status": "success"})



#이메일 중복 확인
@app.route("/join/check_email", methods=["POST"])
def check_email():
    email_receive = request.form['email_give']
    is_exists = maincrud.email_get(email_receive)
    if is_exists:
        return jsonify({'result': 'fail'})
    return jsonify({'result': 'success'})

@app.route("/join/check_nick", methods=["POST"])
def check_nick():
    nick_receive = request.form['nick_give']
    is_exists = maincrud.email_get(nick_receive)
    if is_exists:
        return jsonify({'result': 'fail'})
    return jsonify({'result': 'success'})




@app.route("/login", methods=["POST"])
def login():
    data = json.loads(request.data)
    #로그인에서 데이터는 request data를 불러온다.
    email = data.get("email")
    password = data.get("password")
    #email과 password는 data에서 각각 가져오는데,
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
    #해싱된_비밀번호는 = 이렇게 해싱처리 해준다.
    result = maincrud.login_auth(email,hashed_pw)
    #result는 db에서 email과 hashed_pw를 찾아온 값들로 정의한다.

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
    print(payload['id'])
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
@app.route('/comment', methods=['POST'])
def comment():
    data = json.loads(request.data)
    comment_txt = data.get('text')
    comment_nick = data.get('nick')

    nickname = maincrud.comment_save(comment_nick,comment_txt)
    
    return jsonify({'result': 'success'})

@app.route('/user_load', methods=['GET'])
def user_load():
    users = maincrud.get_user()
    return jsonify({'result': 'success', 'users' : users})

@app.route('/modal', methods=['POST'])
def modal():
    uid = 'dkssud11'
    data = json.loads(request.data)
    idnumber = data.get('idnumber')
    datas = maincrud.userdata(idnumber)
    nick = datas['nick']
    pr_photo = datas['pr_photo']
    comments = maincrud.comment_list(nick)
    
    return jsonify({'result': 'success','datas':datas, 'comments':comments, 'uid':uid})

@app.route('/comment_edit', methods=['POST'])
def comment_edit():
    data = json.loads(request.data)
    cm_number = data.get('cm_number')
    cm_data = maincrud.comment_edit(cm_number)
    
    return jsonify({'cm_data': cm_data})
@app.route('/comment_edit_submit', methods=['POST'])
def comment_edit_submit():
    data = json.loads(request.data)
    cm_number = data.get('cm_number')
    value = data.get('value')
    maincrud.set_comment(cm_number,value)
    
    return jsonify({'result': 'ok'})

@app.route('/pr_edit', methods=['POST'])
def pr_edit():
    data = json.loads(request.data)
    email = data.get('email')
    value = data.get('value')
    maincrud.set_pr(email,value)
    
    return jsonify({'result': 'ok'})    

@app.route('/comment_delete', methods=['POST'])
def comment_delete():
    data = json.loads(request.data)
    cm_number = data.get('cm_number')
    maincrud.delete_comment(cm_number)
    
    return jsonify({'result': 'ok'})

@app.route('/event_page', methods=['GET'])
def event_page():

    users = maincrud.choice()
    print(users)

    return jsonify({'result': 'success', 'category': users})

if __name__ == '__main__':
    print('서버 실행이 완료 되었습니다.')
    app.run('0.0.0.0', port=5001, debug=True, use_reloader=False)

