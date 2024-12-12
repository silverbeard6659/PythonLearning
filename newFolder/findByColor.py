import cv2
import numpy as np
import time
from mss import mss

# Define the region of interest (ROI) on the screen
monitor = {"top": 300, "left": 450, "width": 1000, "height": 700}

# Initialize the screen capture
sct = mss()

# Define the color range in HSV for brown
lower_brown = np.array([9, 100, 10])
upper_brown = np.array([36, 255, 220])

# Variable to store the last time the coordinates were printed
last_print_time = time.time()

def detect_by_color_range(frame, lower_color, upper_color):
    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask using the color range
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # List to store center coordinates
    center_coordinates = []
    
    # Draw rectangles around detected objects and calculate centers
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Calculate the center of the bounding box
        center_x = x + w // 2
        center_y = y + h // 2
        center_coordinates.append((center_x, center_y))
    
    return frame, center_coordinates

def main():
    global last_print_time
    
    while True:
        start_time = time.time()

        try:
            # Capture the screen
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
        except Exception as e:
            print(f"Error capturing screen: {e}")
            break

        # Detect objects by color range in the frame
        result_frame, center_coordinates = detect_by_color_range(frame, lower_brown, upper_brown)

        # Display the result
        cv2.imshow('Screen', result_frame)

        # Check if it's time to print the center coordinates
        current_time = time.time()
        if current_time - last_print_time >= 1.0:
            if center_coordinates:
                print("Center Coordinates of Detected Areas:")
                for i, (center_x, center_y) in enumerate(center_coordinates):
                    print(f"Area {i+1}: ({center_x}, {center_y})")
                
                # Calculate the average center coordinates
                avg_center_x = int(np.mean([coord[0] for coord in center_coordinates]))
                avg_center_y = int(np.mean([coord[1] for coord in center_coordinates]))
                print(f"Average Center Coordinates: ({avg_center_x}, {avg_center_y})")
            else:
                print("No brown areas detected.")
            last_print_time = current_time

        # Maintain 30 FPS
        elapsed_time = time.time() - start_time
        sleep_time = max(0, (1 / 30) - elapsed_time)
        time.sleep(sleep_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
