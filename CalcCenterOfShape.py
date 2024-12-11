# import cv2

# img = cv2.imread("objB.png", 0)
# ret,thresh = cv2.threshold(img,100,255,0)
# im2, contours, hierachy = cv2.findContours(thresh, 1, 2)
# cnt = contours[0]

# M = cv2.moments(cnt)

# cx = int(M['m10']/M['m00'])
# cy = int(M['m01']/M['m00'])

# im2 = cv2.cvtColor(im2, cv2.COLOR_GRAY2RGB)

# cv2.polylines(im2, cnt, True, (0, 0, 255), 2)

# cv2.circle(im2, (cx, cy), 5, (0, 0, 255), 1)

# cv2.imshow("res", im2)

# Найти центр объекта более чем из 3 точек (ну там квадрат)