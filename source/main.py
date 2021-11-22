# Python code for Multiple Color Detection

'''
    HSV Ranges for color :
        - Blue : hMin, sMin, vMin, hMax, sMax, vMax =  116 , 233 , 239 , 120 , 255 , 255
        - Yellow : hMin, sMin, vMin, hMax, sMax, vMax =  29 , 46 , 0 , 35 , 255 , 255
        - Green : hMin, sMin, vMin, hMax, sMax, vMax =  56 , 176 , 64 , 63 , 255 , 255
        - White (add area filter) : hMin, sMin, vMin, hMax, sMax, vMax =  0 , 0 , 255 , 0 , 0 , 255
        - Red : hMin, sMin, vMin, hMax, sMax, vMax =  0 , 60 , 150 , 16 , 255 , 255
        - Orange : hMin, sMin, vMin, hMax, sMax, vMax =  5 , 144 , 33 , 21 , 255 , 255
        - Black (boundaries) : hMin, sMin, vMin, hMax, sMax, vMax =  0 , 0 , 0 , 179 , 255 , 107
'''

import numpy as np
import cv2

imageFrame = cv2.imread('testImage.jpg')

hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

red_lower = np.array([0 , 60 , 150], np.uint8)
red_upper = np.array([16 , 255 , 255], np.uint8)
red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

green_lower = np.array([56 , 176 , 64], np.uint8)
green_upper = np.array([63 , 255 , 255], np.uint8)
green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

blue_lower = np.array([116 , 233 , 239], np.uint8)
blue_upper = np.array([120 , 255 , 255], np.uint8)
blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

orange_lower = np.array([5 , 144 , 33], np.uint8)
orange_upper = np.array([21 , 255 , 255], np.uint8)
orange_mask = cv2.inRange(hsvFrame, orange_lower, orange_upper)

yellow_lower = np.array([29 , 46 , 0], np.uint8)
yellow_upper = np.array([35 , 255 , 255], np.uint8)
yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

white_lower = np.array([0 , 0 , 255], np.uint8)
white_upper = np.array([0 , 0 , 255], np.uint8)
white_mask = cv2.inRange(hsvFrame, white_lower, white_upper)

black_lower = np.array([0 , 0 , 0], np.uint8)
black_upper = np.array([179 , 255 , 107], np.uint8)
black_mask = cv2.inRange(hsvFrame, black_lower, black_upper)

kernal = np.ones((5, 5), "uint8")

red_mask = cv2.dilate(red_mask, kernal)
res_red = cv2.bitwise_and(imageFrame, imageFrame,mask=red_mask)

green_mask = cv2.dilate(green_mask, kernal)
res_green = cv2.bitwise_and(imageFrame, imageFrame,mask=green_mask)

blue_mask = cv2.dilate(blue_mask, kernal)
res_blue = cv2.bitwise_and(imageFrame, imageFrame,mask=blue_mask)

orange_mask = cv2.dilate(orange_mask, kernal)
res_orange = cv2.bitwise_and(imageFrame, imageFrame,mask=orange_mask)

yellow_mask = cv2.dilate(yellow_mask, kernal)
res_yellow = cv2.bitwise_and(imageFrame, imageFrame,mask=yellow_mask)

white_mask = cv2.dilate(white_mask, kernal)
res_white = cv2.bitwise_and(imageFrame, imageFrame,mask=white_mask)

black_dilate = cv2.dilate(black_mask, kernal, iterations=7)
res_black= cv2.bitwise_and(imageFrame, imageFrame,mask=black_mask)
img1 = cv2.bitwise_not(black_dilate, mask = None)
imgRes= cv2.bitwise_and(img1, white_mask)

contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for pic, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if (area > 1000):
        x, y, w, h = cv2.boundingRect(contour)
        imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(imageFrame, "Red", (x + 25, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0)) # changed text color to green for visibility


contours, hierarchy = cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for pic, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if (area > 1000):
        x, y, w, h = cv2.boundingRect(contour)
        imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(imageFrame, "Green", (x + 25, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

contours, hierarchy = cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for pic, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if (area > 1000):
        x, y, w, h = cv2.boundingRect(contour)
        imageFrame = cv2.rectangle(imageFrame, (x, y),(x + w, y + h),(0, 255, 0), 2)
        cv2.putText(imageFrame, "Blue", (x + 25 , y + 25),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255))

contours, hierarchy = cv2.findContours(orange_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for pic, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if (area > 1000):
        x, y, w, h = cv2.boundingRect(contour)
        imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(imageFrame, "Orange", (x + 25, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

contours, hierarchy = cv2.findContours(yellow_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for pic, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if (area > 1000):
        x, y, w, h = cv2.boundingRect(contour)
        imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(imageFrame, "Yellow", (x + 25, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

contours, hierarchy = cv2.findContours(imgRes,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for pic, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if (area > 1000) and (area < 18000):
        x, y, w, h = cv2.boundingRect(contour)
        imageFrame = cv2.rectangle(imageFrame, (x-15, y-15), (x + w + 15, y + h + 15), (0, 255, 0), 2)
        cv2.putText(imageFrame, "White", (x+10, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)

cv2.waitKey(0)
cv2.destroyAllWindows()


