from datetime import datetime, timedelta
from functools import wraps
import hashlib
import json
from bson import ObjectId
from flask import Flask, abort, jsonify, request, Response
from flask_cors import CORS
import jwt
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
    print(comment_txt)
    return jsonify({'message': 'success'})
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)