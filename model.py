import numpy as np
import cv2
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import random
import tensorflow_hub as hub
from tensorflow.keras.models import load_model

model1 = load_model(('static/model/model_pose.h5'), custom_objects={'KerasLayer': hub.KerasLayer})
model2 = load_model(('static/model/model.h5'), custom_objects={'KerasLayer': hub.KerasLayer})
net = cv2.dnn.readNet('static/model/yolov5/yolov5s.onnx')

client = MongoClient('mongodb+srv://test:sparta@cluster0.oaadu.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.joinsport

model = Flask(__name__)


@model.route('/')
def home():
    return render_template('index.html')


@model.route('/fileupload', methods=['POST'])
def file_upload():
    file = request.files['file_give']
    # 해당 파일에서 확장자명만 추출
    extension = file.filename.split('.')[-1]
    # 파일 이름이 중복되면 안되므로, 지금 시간을 해당 파일 이름으로 만들어서 중복이 되지 않게 함!
    find_name = db.joinsport.find_one({'name': "hajin"})
    name = find_name['name']
    # photo = '{name}.{extension}'
    # pwd = request.form['pwd']
    # 파일 저장 경로 설정 (파일은 서버 컴퓨터 자체에 저장됨)
    save_to = f'static/img/{name}.{extension}'
    # 파일 저장!
    file.save(save_to)
    #
    # doc = {
    #     'name': name,
    #     'photo': photo,
    #     'category': ""
    # }
    # db.joinsport.insert_one(doc)

    return jsonify({'result': 'success'})


@model.route('/result')
def result_ct():
    def format_yolov5(frame):

        row, col, _ = frame.shape
        _max = max(col, row)
        result = np.zeros((_max, _max, 3), np.uint8)
        result[0:row, 0:col] = frame
        return result

    all = db.joinsport.find_one({'name': "hajin"})
    photo = all['name']
    image = cv2.imread(f'static/img/{photo}.jpg')
    input_image = format_yolov5(image)  # making the image square
    blob = cv2.dnn.blobFromImage(input_image, 1 / 255.0, (640, 640), swapRB=True)
    net.setInput(blob)
    predictions = net.forward()

    class_ids = []
    confidences = []
    boxes = []

    output_data = predictions[0]

    image_width, image_height, _ = input_image.shape
    x_factor = image_width / 640
    y_factor = image_height / 640

    for r in range(25200):
        row = output_data[r]
        confidence = row[4]
        if confidence >= 0.4:

            classes_scores = row[5:]
            _, _, _, max_indx = cv2.minMaxLoc(classes_scores)
            class_id = max_indx[1]

            if (classes_scores[class_id] > .25):
                confidences.append(confidence)
                class_ids.append(class_id)

                x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)

    class_list = []

    with open("static/model/yolov5/classes.txt", "r") as f:
        class_list = [cname.strip() for cname in f.readlines()]

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45)

    result_class_ids = []
    result_confidences = []
    result_boxes = []

    for i in indexes:
        result_confidences.append(confidences[i])
        result_class_ids.append(class_ids[i])
        result_boxes.append(boxes[i])

    for i in range(len(result_class_ids)):
        box = result_boxes[i]
        class_id = result_class_ids[i]

        cv2.rectangle(image, box, (0, 255, 255), 2)
        cv2.rectangle(image, (box[0], box[1] - 20), (box[0] + box[2], box[1]), (0, 255, 255), -1)
        cv2.putText(image, class_list[class_id], (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0))

    if 34 in result_class_ids:
        # result_learning = False
        # result_ball = False
        # result_ct = "baseball"
        all = list(db.event.find({'category': "baseball"}))
        all_choice = random.choice(all)
        baseball = all_choice['photo']
        result_ct = baseball
        return render_template('event_page.html', category=result_ct, name="hajin", )

    elif 32 in result_class_ids:
        result_learning = False
        result_ball = True
        result_ct = "ball_check"

        x = box[0] + box[2]
        y = box[1] + box[3]
        dst_photo = image[box[1]:y, box[0]:x].copy()
        # cv2.imshow('cut image', dst_photo)
        # cv2.waitKey()

    else:
        result_learning = True
        result_ball = False
        result_ct = "pose_check"



    db.joinsport.update_one({'name': "hajin"}, {"$set": {'category': result_ct}}, upsert=True)


    print(result_class_ids)
    print(result_ct)
    print(result_ball)
    print(result_learning)

    if result_learning == True:
        label_decode = ['baseball', 'basketball', 'soccer', 'volleyball']
        image = cv2.imread('static/img/hajin.jpg')
        image = cv2.resize(image, (224, 224))
        image = np.asarray(image)
        image = image / 255
        image = np.reshape(image, (1, 224, 224, 3))
        pred = model1.predict(image)
        result_ct = label_decode[np.argmax(pred)]
        print(pred)
        print(result_ct)

        if result_ct == "baseball":
            all = list(db.event.find({'category': "baseball"}))
            all_choice = random.choice(all)
            baseball = all_choice['photo']
            result_ct = baseball

        if result_ct == "basketball":
            all2 = list(db.event.find({'category': "basketball"}))
            all_choice2 = random.choice(all2)
            basketball = all_choice2['photo']
            result_ct = basketball

        if result_ct == "soccer":
            all3 = list(db.event.find({'category': "soccer"}))
            all_choice3 = random.choice(all3)
            soccer = all_choice3['photo']
            result_ct = soccer

        if result_ct == "volleyball":
            all4 = list(db.event.find({'category': "volleyball"}))
            all_choice4 = random.choice(all4)
            volleyball = all_choice4['photo']
            result_ct = volleyball

        print(result_ct)

        return render_template('event_page.html', category=result_ct, name="hajin")

    if result_ball == True:

        label_decode = ['baseball', 'basketball', 'soccer', 'volleyball']
        image2 = dst_photo
        image2 = cv2.resize(image2, (224, 224))
        image2 = np.asarray(image2)
        image2 = image2 / 255
        image2 = np.reshape(image2, (1, 224, 224, 3))
        pred2 = model2.predict(image2)
        result_ct = label_decode[np.argmax(pred2)]
        print(pred2)

        if result_ct == "baseball":
            all = list(db.event.find({'category': "baseball"}))
            all_choice = random.choice(all)
            baseball = all_choice['photo']
            result_ct = baseball

        if result_ct == "basketball":
            all2 = list(db.event.find({'category': "basketball"}))
            all_choice2 = random.choice(all2)
            basketball = all_choice2['photo']
            result_ct = basketball

        if result_ct == "soccer":
            all3 = list(db.event.find({'category': "soccer"}))
            all_choice3 = random.choice(all3)
            soccer = all_choice3['photo']
            result_ct = soccer

        if result_ct == "volleyball":
            all4 = list(db.event.find({'category': "volleyball"}))
            all_choice4 = random.choice(all4)
            volleyball = all_choice4['photo']
            result_ct = volleyball

    print(result_ct)
    db.joinsport.update_one({'name': "hajin"}, {"$set": {'category': result_ct}}, upsert=True)
    return render_template('event_page.html', category=result_ct, name="hajin", )


if __name__ == '__main__':
    model.run('0.0.0.0', port=5000, debug=True)
