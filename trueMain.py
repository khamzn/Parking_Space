# -*- coding: cp1251 -*-
import cv2
import pickle
import numpy as np

cap = cv2.VideoCapture(0)

with open('CarPos', 'rb') as f:
    posList = pickle.load(f)

def ckeckParkingSpace(img, list):
    list = [list[i:i + 4] for i in range(0, len(list), 4)]
    spaces=[]

    for i in range(len(list)):
        if len(list[i]) % 4 == 0:
            list2 = np.array(list[i], np.int32)
            list2 = list2.reshape((-1, 1, 2))

            mask = np.zeros(img.shape[:2], dtype="uint8")
            cv2.fillPoly(mask, [list2], (255, 255, 255))

            masked = cv2.bitwise_and(img, img, mask=mask)

            count = cv2.countNonZero(masked)
            cv2.putText(image, str(count), list[i][0], cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
            cv2.putText(image, str(i+1), list[i][2], cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)

            if count<600:
                color = (0, 255, 0)
                thickness = 3
                spaces.append(i+1)
            else:
                color = (0, 0, 255)
                thickness = 2

            cv2.polylines(image, [list2], True, color, thickness=thickness)

    spaces = [str(i) for i in spaces]
    spaces = ','.join(spaces)
    cv2.putText(image, f'empty spaces: {spaces}', (0, 10), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
    return spaces

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, image = cap.read()
    img_post = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_post = cv2.GaussianBlur(img_post, (3,3), 1)
    img_post = cv2.adaptiveThreshold(img_post, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    img_post = cv2.medianBlur(img_post, 5)
    kernel = np.ones((3,3), np.uint8)
    img_post = cv2.dilate(img_post, kernel, iterations=1)

    ckeckParkingSpace(img_post, posList)

    cv2.imshow("Image", image)
    cv2.waitKey(10)