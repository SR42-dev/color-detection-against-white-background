'''
Possible features to add :
    - Mirror image [DONE]
    - Full screen display [DONE]
    - Left-handed/right-handed writing (user input [DONE] or auto detection)
    - Marker thickness trackbar [DONE]
    - Stop writing when not needed [DONE]
'''

import cv2
import numpy as np

def empty(a) :
    pass

cap = cv2.VideoCapture(0) # 0 - default webcam
cap.set(3, 720) # width
cap.set(4, 480) # height
cap.set(10, 150) # brightness

hMin1, sMin1, vMin1, hMax1, sMax1, vMax1 = 0, 167, 93, 11, 255, 217 # HSV limits for colour 1
# hMin2, sMin2, vMin2, hMax2, sMax2, vMax2 = 0, 0, 0, 0, 0, 0 # HSV limits for colour 2

myColors = [['Red', hMin1, sMin1, vMin1, hMax1, sMax1, vMax1]] # add ['colorName', hMin, sMin, vMin, hMax, sMax, vMax] for more colors
myColorValues = [[51, 153, 255]] # add RGB values of marker colours, add ['colorName', R, G, B]
myPoints = [] # [x, y, colorCount(wrt myColorValues), r]

isWrite = 0
isLefty = 0
r = 5 # marker thickness (circle radius)

cv2.namedWindow('Trackbars')  # Creating trackbars to isolate required color
cv2.resizeWindow('Trackbars', 243, 150)
cv2.createTrackbar('Write?', 'Trackbars', 0, 1, empty)
cv2.createTrackbar('Lefty?', 'Trackbars', 0, 1, empty)
cv2.createTrackbar('Thickness', 'Trackbars', 1, 16, empty)

def empty(a):  # argument required
    pass

def findColor(img, myColors, myColorValues) :

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # conversion to HSV from BGR
    count = 0
    newPoints = []
    for color in myColors :
        lower = np.array(color[1:4])  # minimum range array
        upper = np.array(color[4:7])  # maximum range array
        mask = cv2.inRange(imgHSV, lower, upper)  # filtering out colours from HSV image
        x, y = getContours(mask)
        cv2.circle(imgResult, (x,y), r, myColorValues[count], cv2.FILLED) # circle on corner of bounding box
        if x != 0 and y != 0 :
            newPoints.append([x, y, count, r])
        count += 1
        # cv2.imshow(color[0], mask)
    return newPoints

def getContours(img) :

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # image, retrieval method (here, for outermost contours), approximation
    x, y, w, h = 0, 0, 0, 0

    for cnt in contours : # contours - array of contours detected in image

        area = cv2.contourArea(cnt) # finds area of selected contour
        # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3) # image copy, selected contour, (-1 to draw all contours), color, thickness
        if area > 500 : # selects only contours without too much noise (contours with area > 500 units)
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0),3)  # image copy, selected contour, (-1 to draw all contours), color, thickness
            perimeter = cv2.arcLength(cnt, True) # contour, is closed(?)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True) # contour, resolution, is closed(?)
            x, y, w, h = cv2.boundingRect(cnt) # coordinates of each shape
            cv2.rectangle(imgResult, (x,y), (x+w, y+h), (0, 255, 0), 2) # bounding rectangle (green for each detected shape)

    if isLefty == 0 :
        return x+w, y
    else :
        return x, y

def drawOnCanvas(myPoints, myColorValues) :

    for point in myPoints :
        cv2.circle(imgResult, (point[0], point[1]), point[3], myColorValues[point[2]], cv2.FILLED)  # circle on corner of bounding box

while True :
    success, img = cap.read() # <successful execution (boolean)>, <image variable>
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)

    isWrite = cv2.getTrackbarPos('Write?', 'Trackbars')
    isLefty = cv2.getTrackbarPos('Lefty?', 'Trackbars')
    r = cv2.getTrackbarPos('Thickness', 'Trackbars')

    if len(newPoints) != 0 :
        if isWrite == 1:
            for newP in newPoints :
                myPoints.append(newP)

    if len(myPoints) != 0 :
        drawOnCanvas(myPoints, myColorValues)

    finalImage = cv2.flip(imgResult, 1)
    cv2.imshow('Video', finalImage)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
