import cv2
import numpy as np
import time
from mss import mss
import tkinter as tk
from PIL import Image, ImageTk

# Define the region of interest (ROI) on the screen
monitor = {"top": 790, "left": 833, "width": 250, "height": 25}

# Initialize the screen capture
sct = mss()

# Load the template image
try:
    template = cv2.imread('objectB.png', cv2.IMREAD_UNCHANGED)
    if template is None:
        raise ValueError("Template image not found or unable to load.")
    template_height, template_width = template.shape[:2]
    print(f"Template loaded successfully. Shape: {template.shape}")
except Exception as e:
    print(f"Error loading template image: {e}")
    exit()

# Define the color range in HSV for brown
lower_brown = np.array([9, 100, 10])
upper_brown = np.array([36, 255, 220])

def detect_template(frame, template, threshold=0.6):
    if template.shape[2] == 4:
        b, g, r, alpha = cv2.split(template)
        template = cv2.merge((b, g, r))  # Remove alpha channel if present
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + template_width, pt[1] + template_height), (0, 0, 255), 2)
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
        
    def start_fishing(self):
        self.running = True
        print("Starting fishing...")
        self.update_frame()
    
    def stop_fishing(self):
        self.running = False
        print("Stopping fishing...")
    
    def update_frame(self):
        if not self.running:
            return
        
        start_time = time.time()
        
        try:
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
            print(f"Frame captured. Shape: {frame.shape}")
            
            # Detect template
            frame = detect_template(frame, template)
            
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