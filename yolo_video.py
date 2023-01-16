import cv2
import numpy as np
import time


def detect_object(img):
    # construct a blob from the image
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(ln)
    boxes = []
    confidences = []
    classIDs = []
    h, w = img.shape[:2]

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > conf_thresh:
                box = detection[:4] * np.array([w, h, w, h])
                (centerX, centerY, width, height) = box.astype("int")
                x, y = int(centerX - (width / 2)), int(centerY - (height / 2))
                box = [x, y, int(width), int(height)]
                boxes.append(box)
                confidences.append(float(confidence))
                classIDs.append(classID)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    if len(indices) > 0:
        for i in indices.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,255), 2)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            cv2.putText(img, text, (x+5, y+10), cv2.FONT_HERSHEY_PLAIN,1, (0,255,255), 1, cv2.LINE_AA)

    return img, boxes

# load model
net = cv2.dnn.readNetFromDarknet('yolov4-custom.cfg', 'yolov4-custom_best.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
# net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# determine the output layer
ln = net.getLayerNames()
ln = [ln[i- 1] for i in net.getUnconnectedOutLayers()]

conf_thresh = 0.5
LABELS = open('obj.names').readlines()
print(LABELS)
frame_skip = 10
i = 0
prev_frame_time = time.time()

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('http://192.168.1.92:8080/video')
while True:
    success, frame= cap.read()
    frame = cv2.resize(frame, (1280,720))
    if not success:
        print('video frame not found')
        break

    # if i%frame_skip==0:
    img, boxes = detect_object(frame)
    if len(boxes)>0:
        x, y, w, h = boxes[0]
        # print(x,y,w,h)

    t = time.time()
    # print('time=', t-prev_frame_time)
    fps = 1/(t-prev_frame_time)
    # print(fps)
    prev_frame_time = t
    cv2.putText(img, str(round(fps,0)), (10, 10), cv2.FONT_HERSHEY_PLAIN,2, (0,255,255), 1, cv2.LINE_AA)
    cv2.imshow('window', img)
    if cv2.waitKey(1) & 0xFF==27:
        break
    i+=1
cv2.destroyAllWindows()