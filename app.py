import numpy as np
import cv2
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
net = cv2.dnn.readNet('static/model/yolov5/yolov5s.onnx')

client = MongoClient('mongodb+srv://test:sparta@cluster0.oaadu.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.joinsport
#
# user_photo = db.iamge.find_one({'photo': ''})
#
# print(user_photo)



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/fileupload', methods=['POST'])
def file_upload():
    file = request.files['file_give']
    # 해당 파일에서 확장자명만 추출
    extension = file.filename.split('.')[-1]
    # 파일 이름이 중복되면 안되므로, 지금 시간을 해당 파일 이름으로 만들어서 중복이 되지 않게 함!
    name = db.joinsport.find_one({'name':"hajin"})
    photo = name['name']
    filename = f'{photo}'
    all = db.joinsport.find_one({})
    all_number = all['photo']
    all_numbers = len(all_number)
    # 파일 저장 경로 설정 (파일은 서버 컴퓨터 자체에 저장됨)
    save_to = f'static/img/img/{all_numbers}{photo}.{extension}'
    # 파일 저장!
    file.save(save_to)

    doc = {
        'photo': filename
    }
    db.joinsport.insert_one(doc)

### 현재 프로젝트에서는 db에 저장하는 코드 작성 필요! ###

    return jsonify({'result':'success'})


@app.route('/result')
def result_ct():

    def format_yolov5(frame):

        row, col, _ = frame.shape
        _max = max(col, row)
        result = np.zeros((_max, _max, 3), np.uint8)
        result[0:row, 0:col] = frame
        return result

    all = db.joinsport.find_one({'name': "hajin"})
    photo = all['name']
    all = db.joinsport.find_one({})
    all_number = all['photo']
    all_numbers = len(all_number)


    image = cv2.imread(f'static/img/img/{all_numbers}{photo}.jpg')
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


                # elif class_id == 35:

                #     confidences.append(confidence)

                #     class_ids.append(class_id)

                #     x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                #     left = int((x - 0.5 * w) * x_factor)
                #     top = int((y - 0.5 * h) * y_factor)
                #     width = int(w * x_factor)
                #     height = int(h * y_factor)
                #     box2 = np.array([left, top, width, height])
                #     boxes.append(box2)

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

    ###### 볼 체크하기 ########



    # x = box[0] + box[2]
    # y = box[1] + box[3]

    # x2 = box2[0] + box2[2]
    # y2 = box2[1] + box2[3]

    dst_photo = image.copy()
    # dst_photo2 = image[box2[1]:y2, box2[0]:x2].copy()

    if 32 in result_class_ids:
        result_learnig = True
        result_ct = "ball"

        if 32 and 35 in result_class_ids:
            result_learnig = False
            result_ct = "baseball"

        if 34 or 35 in result_class_ids:
            result_learnig = False
            result_ct = "baseball"

    else:
        result_learnig = True
        result_ct = "error"


    print(result_class_ids)
    print(result_ct)



    # cv2.imshow('cut image', dst_photo)
    # cv2.waitKey()

    if result_learnig == True:


        import tensorflow_hub as hub
        from tensorflow.keras.models import load_model
        # from tensorflow.keras import layers
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        import tensorflow as tf
        model = load_model(('static/model/model_pose.h5'), custom_objects={'KerasLayer': hub.KerasLayer})
        # all = db.joinsport.find_one({'name': "hajin"})
        # photo = all['name']

        # model = tf.keras.models.load_model('static/model/model2.h5')

        # model.summary()
        # label_code = {'baseball': 0, 'basketball': 1, 'soccer': 2, 'volleyball': 3}
        label_decode = ['baseball', 'basketball', 'soccer', 'volleyball']

        test_datagen = ImageDataGenerator(rescale=1. / 255)
        test_dir = 'static/img'
        test_generator = test_datagen.flow_from_directory(
            test_dir,
            # target_size 는 학습할때 설정했던 사이즈와 일치해야 함
            target_size=(224, 224),
            color_mode="rgb",
            shuffle=False,

            # test 셋의 경우, 굳이 클래스가 필요하지 않음
            # 학습할때는 꼭 binary 혹은 categorical 로 설정해줘야 함에 유의
            class_mode=None,
            batch_size=1

        )
        pred = model.predict(test_generator)

        # print(pred)
        print(np.argmax(pred[0]))
        result_ct = label_decode[np.argmax(pred[0])]
        print(result_ct)

    return render_template('result.html', result=result_ct)

    # print(dst_photo)
    # cv2.imshow('cut image', dst_photo)
    # cv2.waitKey()
    # cv2.imshow('cut image', dst_photo2)
    # cv2.waitKey()

    # import os
    #
    # try:
    #     os.mkdir('save_image')
    #
    # except:
    #     pass
    #
    # # cv2.imwrite('save_image/1212.jpg', dst_photo2)
    # cv2.imwrite('save_image/ballimage1.jpg', dst_photo)
    #
    #
    # print(result_class_ids)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)