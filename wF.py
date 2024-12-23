import cv2
import pyautogui
import numpy as np
import time
import keyboard  # Import the keyboard library

# Define the region of interest (x, y, width, height)
region = (-1008, 249, 670, 50)  # Example region: x=100, y=100, width=800, height=600

# Load the template image
template = cv2.imread('template.png', 0)
template_height, template_width = template.shape[:2]

def find_template_on_screen(template):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val, max_loc, screenshot

def move_mouse_and_check_template():
    x_start, y_start, width, height = region
    x_end = x_start + width
    y_end = y_start + height
    
    for y in range(y_start, y_end, 10):  # Move down every 10 pixels
        for x in range(x_start, x_end, 10):  # Move right every 10 pixels
            pyautogui.moveTo(x, y, duration=0.001)  # Move faster
            
            # Check if the template is on the screen
            max_val, max_loc, screenshot = find_template_on_screen(template)
            if max_val > 0.8:  # Threshold for template matching
                click_x = x_start + max_loc[0] + template_width // 2
                click_y = y_start + max_loc[1] + template_height // 2
                pyautogui.click(click_x, click_y, button='right')
                
                # Draw rectangle around the matched template
                top_left = max_loc
                bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
                cv2.rectangle(screenshot, top_left, bottom_right, 255, 2)
                
                # Display the screenshot with the matched template
                cv2.imshow('Screenshot', screenshot)
                cv2.waitKey(1000)  # Wait for 1 second to show the rectangle
                cv2.destroyAllWindows()
                
                return True
            if keyboard.is_pressed('q'):  # Check if 'Q' is pressed
                print("Stopping the script...")
                return False
            
            # Display the screenshot without the matched template
            cv2.imshow('Screenshot', screenshot)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Stopping the script...")
                return False
    return False

def main():
    while True:
        if keyboard.is_pressed('q'):  # Check if 'Q' is pressed before starting the loop
            print("Stopping the script...")
            break
        pyautogui.moveTo(region[0], region[1], duration=0.001)  # Move mouse to the start of the region faster
        pyautogui.click(button='left')  # Perform a left click
        pyautogui.press('f')  # Press the 'F' key
        if move_mouse_and_check_template():
            print("Template found and right-clicked.")
        else:
            print("Template not found.")

if __name__ == "__main__":
    main()
