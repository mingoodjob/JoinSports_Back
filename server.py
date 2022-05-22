from datetime import datetime, timedelta
from functools import wraps
import hashlib
import json
from bson import ObjectId
from flask import Flask, abort, jsonify, request, Response
from flask_cors import CORS
import jwt,maincrud
from pymongo import MongoClient


# maincrud.save('hello@hello.com','hello','최재완','1.jpg','baseball')

# name = '이민기'
# get_id = maincrud.nickread(name)
# print(get_id)
# maincrud.pr_desc_set('김하진','요리하기')

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

    maincrud.comment_save(comment_txt)
    return jsonify({'result': 'success'})

@app.route('/user_load', methods=['GET'])
def user_load():
    users = maincrud.get_user()
    return jsonify({'result': 'success', 'users' : users})

@app.route('/modal', methods=['POST'])
def modal():
    data = json.loads(request.data)
    idnumber = data.get('idnumber')
    datas = maincrud.userdata(idnumber)
    
    return jsonify({'result': 'success','datas':datas})

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)