import pickle
import cv2
import numpy as np

try:
    with open('CarPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

cap = cv2.VideoCapture(0)
for i in range(2):
    succes, img = cap.read()


def mouseClick(events, x, y, flags, params):
    global img
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append([x, y])
    if events == cv2.EVENT_RBUTTONDOWN:
        for i in range(len(posList)):
            posList.pop(0)
        cv2.destroyAllWindows()
        for i in range(2):
            succes, img = cap.read()

    with open('CarPos', 'wb') as f:
        pickle.dump(posList, f)

def poly(imgPoly, list):
    list = [list[i:i + 4] for i in range(0, len(list), 4)]

    for i in range(len(list)):
        if len(list[i])%4 == 0:
            list2 = np.array(list[i], np.int32)
            list2 = list2.reshape((-1, 1, 2))
            cv2.polylines(imgPoly, [list2], True, (255, 0, 0), thickness=2)


while True:
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    poly(img, posList)
    cv2.waitKey(1)
