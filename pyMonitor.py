import cv2
import numpy as np
import pyautogui
import time

# Load the pattern image
pattern_image = cv2.imread('obj3.png', cv2.IMREAD_GRAYSCALE)
pattern_height, pattern_width = pattern_image.shape

# Define a function to monitor the screen
def monitor_screen():
    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Perform template matching
        result = cv2.matchTemplate(screenshot_gray, pattern_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Set a threshold for detection
        locations = np.where(result >= threshold)

        # Draw rectangles around matched regions
        for pt in zip(*locations[::-1]):  # Switch columns and rows
            cv2.rectangle(screenshot, pt, (pt[0] + pattern_width, pt[1] + pattern_height), (0, 255, 0), 2)
        
        screenshotS = cv2.resize(screenshot,(960,540))
        # Display the result
        cv2.imshow('Screen Monitor', screenshotS)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# Start monitoring the screen
monitor_screen()