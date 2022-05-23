# import tensorflow_hub as hub
# from tensorflow.keras.models import load_model
# # from tensorflow.keras import layers
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# import numpy as np
# import tensorflow as tf
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.oaadu.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.joinsport
# model = tf.keras.models.load_model('static/model/modetestl.h5')
doc = {
    'test' : "test",
    'hi' : "hi"
}
db.joinsport.insert(doc)
a = db.joinsport.find_one({})
b = a['photo']
c = len(b)

print(a)
print(b)
print(c)