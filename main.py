# -*- coding: cp1251 -*-
import cv2
import pickle
import numpy as np
import sqlite3

def listCameraIndexes() -> list:
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if cap.isOpened():
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            print(f'*  [{index}] video_{width:.0f}x{height:.0f}')
            arr.append(index)
        index += 1
        i -= 1
    return arr

print("List of available cameras:")
camerasList : list = listCameraIndexes()
print()
cameraIndex : int = -1
while True:
    print("Select the camera to work with (see the cameras list above, enter -1 to exit):")
    cameraIndex : int = int(input())
    if cameraIndex == -1:
        exit(0)
    if cameraIndex in camerasList:
        break
    print(f'Sorry, camera {cameraIndex} is not in the available cameras list {camerasList}')

cap = cv2.VideoCapture(cameraIndex)

value = 0.13

with open('CarPos', 'rb') as f:
    posList = pickle.load(f)


def check_space(img, posList):
    posList = [posList[i:i + 4] for i in range(0, len(posList), 4)]
    spaces = []

    for i in range(len(posList)):
        if len(posList[i]) % 4 == 0:
            pos = np.array(posList[i], np.int32)
            pos = pos.reshape((-1, 1, 2))

            mask = np.zeros(img.shape[:2], dtype="uint8")
            cv2.fillPoly(mask, [pos], (255, 255, 255))

            masked = cv2.bitwise_and(img, img, mask=mask)

            count = cv2.countNonZero(masked)
            cv2.putText(image, str(count/cv2.contourArea(pos)), posList[i][0], cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
            #cv2.putText(image, str(i+1), posList[i][2], cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

            if count/cv2.contourArea(pos) < value:
                color = (0, 255, 0)
                thickness = 3
                spaces.append(i+1)
            else:
                color = (0, 0, 255)
                thickness = 2

            cv2.polylines(image, [pos], True, color, thickness=thickness)

    spaces = [str(i) for i in spaces]
    spl = spaces
    spaces = ','.join(spaces)
    cv2.putText(image, f'empty spaces: {spaces}', (0, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 1)
    return spl


def insert_to_db(content, path):
    conn = sqlite3.connect(path)
    conn.execute(f'INSERT INTO spaces(id) VALUES ("{content}")')
    conn.commit()
    conn.close()


def delete_db(path):
    conn = sqlite3.connect(path)
    conn.execute('DELETE FROM spaces')
    conn.commit()
    conn.close()


def post():
    delete_db("server/instance/database_parking.db")
    for i in check_space(img_post, posList):
        insert_to_db(int(i), 'server/instance/database_parking.db')


def image_processing(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (3, 3), 1)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    image = cv2.medianBlur(image, 5)
    kernel = np.ones((3, 3), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)

    return image


while True:

    #if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
    #    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, image = cap.read()
    img_post = image_processing(image)

    post()

    cv2.imshow("Image", image)
    
    if cv2.waitKey(10) == 27:
        break
