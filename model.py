import numpy as np
import cv2
import os
import random
import tensorflow_hub as hub
from tensorflow.keras.models import load_model
import urllib
import certifi

def model_load():

    global model1,model2,net

    os.environ['HOME']
    model1 = load_model(('./static/model/model_pose.h5'), custom_objects={'KerasLayer': hub.KerasLayer})
    model2 = load_model(('./static/model/model.h5'), custom_objects={'KerasLayer': hub.KerasLayer})
    net = cv2.dnn.readNet('static/model/yolov5/yolov5s.onnx')

def result_ct(photo):

    def format_yolov5(frame):

        row, col, _ = frame.shape
        _max = max(col, row)
        result = np.zeros((_max, _max, 3), np.uint8)
        result[0:row, 0:col] = frame
        return result

    image = cv2.imread(f'static/img/{photo}')
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
        # all_choice = random.choice(all) #이미지 랜덤
        # baseball = all_choice['photo']
        result_ct = 'baseball'
        return result_ct

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

    if result_learning == True:
        label_decode = ['baseball', 'basketball', 'soccer', 'volleyball']
        image = cv2.imread(f'static/img/{photo}')
        image = cv2.resize(image, (224, 224))
        image = np.asarray(image)
        image = image / 255
        image = np.reshape(image, (1, 224, 224, 3))
        pred = model1.predict(image)
        result_ct = label_decode[np.argmax(pred)]

        return result_ct

    if result_ball == True:

        label_decode = ['baseball', 'basketball', 'soccer', 'volleyball']
        image2 = dst_photo
        image2 = cv2.resize(image2, (224, 224))
        image2 = np.asarray(image2)
        image2 = image2 / 255
        image2 = np.reshape(image2, (1, 224, 224, 3))
        pred2 = model2.predict(image2)
        result_ct = label_decode[np.argmax(pred2)]

    return result_ct
