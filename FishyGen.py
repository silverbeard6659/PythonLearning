import cv2
import pyautogui
import time
import numpy as np

def find_object(template_path, screenshot, threshold):
    """
    Finds the center of an object in the screenshot using template matching.

    Parameters:
    - template_path: Path to the template image to match.
    - screenshot: Grayscale screenshot image.
    - threshold: Matching threshold value.

    Returns:
    - Tuple (center_x, center_y) if the object is found, otherwise None.
    - Rectangle coordinates (x, y, w, h) if the object is found, otherwise None.
    """
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    # Get the center of the detected object
    if len(loc[0]) > 0:
        top_left = (min(loc[1]), min(loc[0]))
        bottom_right = (max(loc[1]), max(loc[0]))
        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]
        center_x = top_left[0] + width // 2
        center_y = top_left[1] + height // 2
        return (center_x, center_y), (top_left[0], top_left[1], width, height)
    else:
        return None, None

def main():
    while True:
        # Step 1: Wait for 3 seconds before starting
        print("Waiting for 3 seconds...")
        time.sleep(3)

        # Step 2: Hover mouse over the center of the screen
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        print(f"Moving mouse to the center of the screen: ({center_x}, {center_y})")
        pyautogui.moveTo(center_x, center_y)

        # Step 3: Press '1'
        print("Pressing '1'...")
        pyautogui.press('1')

        # Step 4: Detect pattern image - object1.png on screen and then press '1'
        screenshot = pyautogui.screenshot()
        screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        screenshot_color = np.array(screenshot)
        object1_location, _ = find_object('object1.png', screenshot_gray, threshold=0.8)
        if object1_location:
            print(f"Object1 found at: {object1_location}")
            pyautogui.press('1')
        else:
            print("Object1 not found. Restarting the loop...")
            continue  # If object1 is not found, restart the loop

        # Step 5: Detect two items simultaneously - object2 and object3 with different thresholds
        object2_location, object2_rect = find_object('object2.png', screenshot_gray, threshold=0.5)
        object3_location, object3_rect = find_object('object3.png', screenshot_gray, threshold=0.8)
        print(f"Object2 location: {object2_location}")
        print(f"Object3 location: {object3_location}")

        # Step 6: Continuously hold '2' or '3' as long as object2 and object3 are present
        while object2_location and object3_location:
            print(f"Object2 Center: {object2_location}")
            print(f"Object3 Center: {object3_location}")

            # Step 7 & 8: Hold '2' or '3' based on coordinates
            if object2_location[0] < object3_location[0]:
                print("Holding '2' because Object2 is to the left of Object3...")
                pyautogui.keyDown('2')
                pyautogui.keyUp('3')  # Ensure '3' is not held
            elif object2_location[0] > object3_location[0]:
                print("Holding '3' because Object2 is to the right of Object3...")
                pyautogui.keyDown('3')
                pyautogui.keyUp('2')  # Ensure '2' is not held

            # Draw rectangles around detected objects
            if object2_rect:
                x, y, w, h = object2_rect
                cv2.rectangle(screenshot_color, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if object3_rect:
                x, y, w, h = object3_rect
                cv2.rectangle(screenshot_color, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Display the screenshot with rectangles
            # cv2.imshow('Detected Objects', screenshot_color)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     cv2.destroyAllWindows()
            #     return  # Exit the program if 'q' is pressed

            # Take another screenshot and check for objects again
            screenshot = pyautogui.screenshot()
            screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
            screenshot_color = np.array(screenshot)
            object2_location, object2_rect = find_object('object2.png', screenshot_gray, threshold=0.5)
            object3_location, object3_rect = find_object('object3.png', screenshot_gray, threshold=0.8)
            print(f"Object2 location: {object2_location}")
            print(f"Object3 location: {object3_location}")

            time.sleep(1)  # Check every second

        # Release the keys if objects are no longer detected
        pyautogui.keyUp('2')
        pyautogui.keyUp('3')
        print("Objects no longer detected. Releasing keys and restarting the loop...")

        # Close the OpenCV window
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()