# from flask import Flask, render_template, request, jsonify
# from bs4 import BeautifulSoup
from pymongo import MongoClient
# from datetime import datetime
# import requests
import certifi
# import random

client = MongoClient('mongodb+srv://test:sparta@cluster0.avef3.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.joinsports

def save(email,pwd,nick,pr_photo,category):  
    
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
    
def nickread(nick):
    
    data_col = db.user
    all_data = data_col.find_one({'nick': nick})
    id_value = all_data['_id']
    
    return id_value

def comment_save(comment):

    doc = {
        'nick' : '헬로우',
        'comment' : comment

    }
    
    data_col = db.comment
    data_col.insert_one(doc)

def pr_desc_set(nick,pr_desc):

    data_col = db.user
    data_col.update_one({'nick' : nick}, {"$set":{"pr_desc" :pr_desc}})

def abcd(): 
    save('hello@hello.com','hello','김하진','1.jpg','baseball')
    get_id = nickread('이민기')
    print(get_id)


