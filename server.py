from datetime import datetime, timedelta
import hashlib
import json
import jwt,maincrud
from bson import ObjectId
from flask import Flask, abort, jsonify, request, Response
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
cors = CORS(app, resources={
            r'*': {'origins': ['http://127.0.0.1:4000', 'http://127.0.0.1:5500']}})

@app.route('/')
def home():
    return 'REST API'

@app.route('/comment', methods=['POST'])
def comment():
    data = json.loads(request.data)
    comment_txt = data.get('text')
    comment_nick = data.get('nick')

    nickname = maincrud.comment_save(comment_nick,comment_txt)
    
    return jsonify({'result': 'success', 'nickname':nickname[0],'pr_photo':nickname[1]})

@app.route('/user_load', methods=['GET'])
def user_load():
    users = maincrud.get_user()
    return jsonify({'result': 'success', 'users' : users})

@app.route('/modal', methods=['POST'])
def modal():
    uid = '1'
    data = json.loads(request.data)
    idnumber = data.get('idnumber')
    print(idnumber)
    datas = maincrud.userdata(idnumber)
    nick = datas['nick']
    pr_photo = datas['pr_photo']
    comments = maincrud.comment_list(nick)
    
    return jsonify({'result': 'success','datas':datas, 'comments':comments})

@app.route('/comment_edit', methods=['POST'])
def comment_edit():
    data = json.loads(request.data)
    cm_number = data.get('cm_number')
    cm_data = maincrud.comment_edit(cm_number)
    print(cm_data)
    
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
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)