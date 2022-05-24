import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow_hub as hub
from tensorflow.keras.models import load_model
import cv2
from cv2 import imread, imshow, resize
from flask import Flask, render_template, request, redirect, url_for, jsonify

import tensorflow as tf
from pymongo import MongoClient
# client = MongoClient('mongodb+srv://test:sparta@cluster0.oaadu.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.joinsport
# model = tf.keras.models.load_model('static/model/modetestl.h5')
# all = db.joinsport.find_one({'name': "hajin"})
# name = all['name']
# print(name)

model = load_model(('static/model/model_pose.h5'), custom_objects={'KerasLayer': hub.KerasLayer})

label_decode = ['baseball', 'basketball', 'soccer', 'volleyball']
image = cv2.imread('static/img/img/5hajin.jpg')
image = cv2.resize(image,(224,224))
image = np.asarray(image)
image = image / 255
image = np.reshape(image, (1, 224, 224, 3))
pred = model.predict(image)
result_ct = label_decode[np.argmax(pred)]

print(result_ct)


# def model2():
#     label_decode = ['baseball', 'basketball', 'soccer', 'volleyball']
#     image = cv2.imread('static/img/img/5hajin.jpg')
#     image = cv2.resize(image, (224, 224))
#     image = np.asarray(image)
#     image = image / 255
#     image = np.reshape(image, (1, 224, 224, 3))
#     pred = model.predict(image)
#     result_ct = label_decode[np.argmax(pred)]
#
#     print(result_ct)
#
#     return render_template('result.html',category=result_ct)
