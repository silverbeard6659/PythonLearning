import cv2
import numpy as np
import math

img = cv2.imread("objB.png")

b,g,r = cv2.split(img)

smoothed = cv2.GaussianBlur(g, (3,3), 0)

edges = cv2.Canny(smoothed, 15, 60, apertureSize = 3)

lines = cv2.HoughLinesP(edges,1,np.pi/180,35, 30, 20)


print("length of lines detected ", lines.shape)


for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)
        print("x1,y1", x1,",",y1, " --- ", "x2,y2", x2,",",y2)



cv2.imshow('detected',img)
cv2.waitKey(0)
cv2.destroyAllWindows()