import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow_hub as hub
from tensorflow.keras.models import load_model
import cv2

from cv2 import imread, imshow, resize

import tensorflow as tf
from pymongo import MongoClient
# client = MongoClient('mongodb+srv://test:sparta@cluster0.oaadu.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.joinsport
# model = tf.keras.models.load_model('static/model/modetestl.h5')
# all = db.joinsport.find_one({'name': "hajin"})
# name = all['name']
# print(name)

model = load_model(('static/model/model_pose.h5'), custom_objects={'KerasLayer': hub.KerasLayer})
image = cv2.imread('static/img/img/5hajin.jpg')
image = cv2.resize(image,(224,224))
cv2_imshow = image
image = np.asarray(image)
image = image / 255
image = np.reshape(image, (1, 224, 224, 3))
print(model.predict(image))
classes = [np.argmax(model.predict(image))]
print(classes)