import cv2
import numpy as np
import time
from mss import mss

# Define the region of interest (ROI) on the screen
monitor = {"top": 300, "left": 450, "width": 1000, "height": 700}

# Initialize the screen capture
sct = mss()

# Load the template image
try:
    # Specify the full path to the template image if it's not in the same directory
    template = cv2.imread('objectC.png', cv2.IMREAD_UNCHANGED)  # Change to '/path/to/your/objectB.png' if needed
    if template is None:
        raise ValueError("Template image not found or unable to load.")
    template_height, template_width = template.shape[:2]
except Exception as e:
    print(f"Error loading template image: {e}")
    exit()

def detect_template(frame, template, threshold=0.5):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Check if the template has an alpha channel
    if template.shape[2] == 4:
        # Split the template into B, G, R, and A channels
        b, g, r, alpha = cv2.split(template)
        # Convert the template to grayscale using the alpha channel
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
        # Apply the alpha channel to the grayscale template
        template = cv2.bitwise_and(template_gray, template_gray, mask=alpha)
    else:
        # Convert the template to grayscale
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    # Perform template matching
    result = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
    
    # Find locations where the match is above the threshold
    loc = np.where(result >= threshold)
    
    # Draw rectangles around detected objects
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + template_width, pt[1] + template_height), (0, 0, 255), 2)
    
    return frame

def main():
    while True:
        start_time = time.time()

        try:
            # Capture the screen
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
        except Exception as e:
            print(f"Error capturing screen: {e}")
            break

        # Detect the template in the frame
        result_frame = detect_template(frame, template)

        # Display the result
        cv2.imshow('Screen', result_frame)

        # Maintain 30 FPS
        elapsed_time = time.time() - start_time
        sleep_time = max(0, (1 / 30) - elapsed_time)
        time.sleep(sleep_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
