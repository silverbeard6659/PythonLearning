import cv2
import pyautogui
import time
import numpy as np

def find_object(template_path, screenshot):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    # Get the center of the detected object
    if len(loc[0]) > 0:
        center_x = int((loc[1][0] + loc[1][-1]) / 2)
        center_y = int((loc[0][0] + loc[0][-1]) / 2)
        return (center_x, center_y)
    else:
        return None

def main():
    while True:
        # Step 1: Wait for 3 seconds before starting
        time.sleep(3)

        # Step 2: Hover mouse over the center of the screen
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        pyautogui.moveTo(center_x, center_y)

        # Step 3: Press '1'
        pyautogui.press('1')

        # Step 4: Detect pattern image - object1.png on screen and then press '1'
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        object1_location = find_object('object1.png', screenshot)

        if object1_location:
            pyautogui.press('1')
        else:
            continue  # If object1 is not found, restart the loop

        # Step 5: Detect two items simultaneously - object2 and object3
        object2_location = find_object('object2.png', screenshot)
        object3_location = find_object('object3.png', screenshot)

        start_time = time.time()

        while not (object2_location and object3_location):
            if time.time() - start_time > 7:
                break  # Restart the loop if no objects are found within 7 seconds

            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
            object2_location = find_object('object2.png', screenshot)
            object3_location = find_object('object3.png', screenshot)

            time.sleep(1)  # Check every second

        if not (object2_location and object3_location):
            continue  # If no objects are found within 7 seconds, restart the loop

        # Step 6: Print coordinates of center object2 and center object3
        print(f"Object2 Center: {object2_location}")
        print(f"Object3 Center: {object3_location}")

        # Step 7 & 8: Hold '2' or '3' based on coordinates
        if object2_location[0] < object3_location[0]:
            pyautogui.keyDown('2')
        elif object2_location[0] > object3_location[0]:
            pyautogui.keyDown('3')

        # Optionally, you can add a condition to release the key after some time or event
        # For now, it will keep holding the key until the program is stopped manually

if __name__ == "__main__":
    main()