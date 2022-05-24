from flask import Flask, jsonify, request
import json
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.avef3.mongodb.net/?retryWrites=true&w=majority')
db = client.joinsports


@app.route("/category", methods=['POST'])
def find_category():
    category = json.loads(request.data)

    category_users = list(db.user.find({'category': category['category']}))
    for category_user in category_users:
        category_user["_id"] = str(category_user["_id"])

    return jsonify({"message": "success", "category_users": category_users})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
