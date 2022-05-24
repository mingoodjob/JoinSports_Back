from pymongo import MongoClient
import certifi,base64,requests,string,random,os
from bson import ObjectId

client = MongoClient('mongodb+srv://test:sparta@cluster0.avef3.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.joinsports

def user_save(email,pwd,nick,pr_photo,category):  
    
    doc = {
    
        'email': email,
        'pwd': pwd,
        'nick': nick,
        'pr_photo' : pr_photo,
        'category' : category,
        'pr_desc' : ''
    
    }

    data_col = db.user
    data_col.insert_one(doc)
    
def get_user():

    col = db.user
    users = col.aggregate([{ "$sample": { "size": 9 } }])
    result = []
    
    for user in users:
        user["_id"] = str(user["_id"])
        result.append(user)
        
    return result

def email_get(email):
    
    col = db.user
    is_exists = col.find_one({'email': email})

    return is_exists

def nick_get(nick):
    
    col = db.user
    is_exists = col.find_one({'nick': nick})

    return is_exists
    
def login_auth(email, password):
    
    col = db.user

    result = col.find_one({
        'email': email,
        'pwd': password
    })

    return result

def userdata(idnumber):
    
    data_user = db.user
    
    data = data_user.find_one({'_id': ObjectId(idnumber)})
    data["_id"] = str(data["_id"])
    print(type(data["_id"]))
    
    return data

def userid(email):

    data_user = db.user
    
    data = data_user.find_one({'email': email})

    nick = data["nick"]

    return nick


def comment_list(nick):
    data_comment = db.comment
    comment_lists = data_comment.find({'comment_id': nick})
    
    result = []
    
    for comment in comment_lists:
        comment['_id'] = str(comment['_id'])
        result.append(comment)
    
    return result

def comment_save(comment_id,comment):
    nick = '이민기'

    data_col = db.comment
    db_user = db.user
    
    user = db_user.find_one({'nick': nick})
    pr_photo = user['pr_photo']

    doc = {
        'comment_id' : comment_id,
        'nick' : nick,
        'comment' : comment,
        'pr_photo' : pr_photo,
        'date' : '10초전'
    }
    
    data_col.insert_one(doc)
    
    
    nickname = db_user.find_one({'nick':nick},{'_id':0})
    
    return nick
    

def pr_desc_set(nick,pr_desc):

    data_col = db.user
    data_col.update_one({'nick' : nick}, {"$set":{"pr_desc" :pr_desc}})

def img_save(req_file):
    req_file = req_file

    with open(req_file, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": 'd889e8da87c9070b622a1dc576797216',
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)
        filename = res.json()['data']['url']
        
        return filename
        
def random_string():

    number_of_strings = 1
    length_of_string = 15
    for x in range(number_of_strings):
        ran_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        
        return ran_str

def comment_edit(cm_data):
    
    data_comment = db.comment
    
    data = data_comment.find_one({'_id': ObjectId(cm_data)})
    data["_id"] = str(data["_id"])
    
    return data
    
def set_comment(cm_data,value):
    data_comment = db.comment
    data_comment.update_one({'_id': ObjectId(cm_data)}, {"$set":{"comment" :value}})
    
def delete_comment(cm_number):
    data_comment = db.comment
    data_comment.delete_one({"_id":ObjectId(cm_number)})

def set_pr(email,value):
    data_user = db.user
    data_user.update_one({'email': email},{"$set":{"pr_desc" : value}})
    
def random_user(category):
    users = db.user.aggregate([
    {"$match" : {"category":category}}, 
    {"$sample": {"size": 9}} 
    ]);

    result = []
    
    for user in users:
        user['_id'] = str(user['_id'])
        result.append(user)

    return result

# file_list = os.listdir('./img')

# for i in file_list:
#     print(i)
#     ran_str = random_string()
#     fileurl = img_save(f'./img/{i}')
#     email = f'{ran_str}@naver.com'
#     pwd = ran_str
#     nick = ran_str
#     pr_photo = fileurl
#     category = 'base_ball'
#     user_save(email,pwd,nick,pr_photo,category)

# col = db.user

# data = col.find({},{'_id': 0})
# for i in data:
#     print(i['pr_photo'])

# userdata('6289da8ede9df517e22b4002')