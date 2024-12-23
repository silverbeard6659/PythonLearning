import cv2
import numpy as np
import time
from mss import mss
import tkinter as tk
from PIL import Image, ImageTk
import pyautogui

# Define the regions of interest (ROIs) on the screen
monitor_objectB = {"top": 790, "left": 833, "width": 250, "height": 25}
monitor_objectA = {"top": 100, "left": 100, "width": 200, "height": 200}  # Adjust these values as needed

# Initialize the screen capture
sct = mss()

# Load the template images
try:
    template_objectB = cv2.imread('objectB.png', cv2.IMREAD_UNCHANGED)
    if template_objectB is None:
        raise ValueError("Template image objectB.png not found or unable to load.")
    templateB_height, templateB_width = template_objectB.shape[:2]
    print(f"Template objectB loaded successfully. Shape: {template_objectB.shape}")
    
    # Ensure template is in BGR format and 8-bit unsigned integer
    if template_objectB.shape[2] == 4:
        b, g, r, alpha = cv2.split(template_objectB)
        template_objectB = cv2.merge((b, g, r))
    if template_objectB.dtype != np.uint8:
        template_objectB = cv2.convertScaleAbs(template_objectB)
    
    template_objectA = cv2.imread('objectA.png', cv2.IMREAD_UNCHANGED)
    if template_objectA is None:
        raise ValueError("Template image objectA.png not found or unable to load.")
    templateA_height, templateA_width = template_objectA.shape[:2]
    print(f"Template objectA loaded successfully. Shape: {template_objectA.shape}")
    
    # Ensure template is in BGR format and 8-bit unsigned integer
    if template_objectA.shape[2] == 4:
        b, g, r, alpha = cv2.split(template_objectA)
        template_objectA = cv2.merge((b, g, r))
    if template_objectA.dtype != np.uint8:
        template_objectA = cv2.convertScaleAbs(template_objectA)
    
except Exception as e:
    print(f"Error loading template image: {e}")
    exit()

# Define the color range in HSV for brown
lower_brown = np.array([9, 100, 10])
upper_brown = np.array([36, 255, 220])

def detect_template(frame, template, threshold=0.6):
    # Ensure frame is in BGR format and 8-bit unsigned integer
    if frame.shape[2] == 4:
        b, g, r, alpha = cv2.split(frame)
        frame = cv2.merge((b, g, r))
    if frame.dtype != np.uint8:
        frame = cv2.convertScaleAbs(frame)
    
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 0, 255), 2)
    return frame

def detect_by_color_range(frame, lower_color, upper_color):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center_coordinates = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center_x = x + w // 2
        center_y = y + h // 2
        center_coordinates.append((center_x, center_y))
    return frame, center_coordinates

def wait_for_objectA(label):
    print("Waiting for objectA.png to appear...")
    while True:
        screenshot = np.array(sct.grab(monitor_objectA))
        if screenshot.shape[2] == 4:
            b, g, r, alpha = cv2.split(screenshot)
            screenshot = cv2.merge((b, g, r))
        if screenshot.dtype != np.uint8:
            screenshot = cv2.convertScaleAbs(screenshot)
        
        result = cv2.matchTemplate(screenshot, template_objectA, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        if max_val >= 0.6:  # Adjust threshold as needed
            print("objectA.png detected!")
            pyautogui.press('1')
            label.config(text="objectA.png detected!")
            return
        
        # Display the current frame in the label
        screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(screenshot_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.config(image=imgtk)
        
        time.sleep(0.1)  # Check every 100ms

class FishingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fishing Bot for GW2")
        
        self.label = tk.Label(root)
        self.label.pack()
        
        self.running = False
        self.start_button = tk.Button(root, text="Start", command=self.start_fishing)
        self.start_button.pack(side=tk.LEFT)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_fishing)
        self.stop_button.pack(side=tk.RIGHT)
        
        # Create a separate window for monitoring objectA
        self.objectA_window = tk.Toplevel(root)
        self.objectA_window.title("ObjectA Monitor")
        self.objectA_label = tk.Label(self.objectA_window)
        self.objectA_label.pack()
        self.objectA_status_label = tk.Label(self.objectA_window, text="Waiting for objectA.png...")
        self.objectA_status_label.pack()
        
    def start_fishing(self):
        self.running = True
        print("Starting fishing...")
        
        # Move mouse to center of screen
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width // 2, screen_height // 2)
        
        # Press key '1'
        pyautogui.press('1')
        
        # Wait for objectA.png to appear in a separate thread
        import threading
        thread = threading.Thread(target=wait_for_objectA, args=(self.objectA_label,))
        thread.daemon = True
        thread.start()
        
        # Start updating frames
        self.update_frame()
    
    def stop_fishing(self):
        self.running = False
        print("Stopping fishing...")
    
    def update_frame(self):
        if not self.running:
            return
        
        start_time = time.time()
        
        try:
            screenshot = np.array(sct.grab(monitor_objectB))
            frame = screenshot
            print(f"Frame captured. Shape: {frame.shape}, Type: {frame.dtype}")
            
            # Ensure frame is in BGR format and 8-bit unsigned integer
            if frame.shape[2] == 4:
                b, g, r, alpha = cv2.split(frame)
                frame = cv2.merge((b, g, r))
            if frame.dtype != np.uint8:
                frame = cv2.convertScaleAbs(frame)
            
            # Detect template
            frame = detect_template(frame, template_objectB)
            
            # Detect by color range
            frame, center_coordinates = detect_by_color_range(frame, lower_brown, upper_brown)
            
            # Convert frame to RGB for displaying in Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.config(image=imgtk)
        except Exception as e:
            print(f"Error processing frame: {e}")
        
        # Maintain 30 FPS
        elapsed_time = time.time() - start_time
        sleep_time = max(0, (1 / 30) - elapsed_time)
        self.root.after(int(sleep_time * 1000), self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = FishingBotApp(root)
    root.mainloop()
