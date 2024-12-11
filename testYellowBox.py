import cv2

image = cv2.imread("ybox.jpg")
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_yellow = (22,100,20)
upper_yellow = (35,255,255)
mask = cv2.inRange(image_hsv, lower_yellow, upper_yellow)

cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i, c in enumerate(cnts[0]):
    # compute the center of the contour
    M = cv2.moments(c)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    print(f"Yellow Box {i} : cx={cx}, cx={cy}") 
    cv2.imshow('screen',image)