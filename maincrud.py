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
    users = list(col.find())
    for user in users:
        user["_id"] = str(user["_id"])
        print(str(user["_id"]))
        
    return users

def random_user():
    pass
    
def userdata(idnumber):
    
    data_col = db.user
    data = data_col.find_one({'_id': ObjectId(idnumber)})
    data["_id"] = str(data["_id"])
       
    return data

def comment_save(comment):

    doc = {
        'comment_id' : '',
        'nick' : '헬로우',
        'comment' : comment

    }
    
    data_col = db.comment
    data_col.insert_one(doc)

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
        
        print(filename)
        return filename
        
def random_string():

    number_of_strings = 1
    length_of_string = 15
    for x in range(number_of_strings):
        ran_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        
        return ran_str


# get_user()


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