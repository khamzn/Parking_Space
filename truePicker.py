import pickle
import cv2
import numpy as np

try:
    with open('CarPosT', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

img = cv2.imread('images/carParkImg.png')

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append([x, y])
    if events == cv2.EVENT_RBUTTONDOWN:
        for i in range(len(posList)):
            posList.pop(0)
            cv2.destroyAllWindows()

    with open('CarPosT', 'wb') as f:
        pickle.dump(posList, f)

def poly(imgPoly, list):
    list = [list[i:i + 4] for i in range(0, len(list), 4)]

    for i in range(len(list)):
        if len(list[i])%4 == 0:
            print(list[i])
            list2 = np.array(list[i], np.int32)
            list2 = list2.reshape((-1, 1, 2))
            cv2.polylines(imgPoly, [list2], True, (255, 0, 0))

while True:
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    poly(img, posList)
    cv2.waitKey(1)