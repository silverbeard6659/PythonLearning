import pyautogui
import keyboard

def print_cursor_coordinates():
    while True:
        if keyboard.is_pressed('v'):
            # Get the current mouse position
            x, y = pyautogui.position()
            print(f"Cursor Coordinates: ({x}, {y})")
            # Wait for the key to be released to avoid multiple prints
            while keyboard.is_pressed('v'):
                pass

if __name__ == "__main__":
    print("Press 'v' to print cursor coordinates. Press 'q' to quit.")
    try:
        print_cursor_coordinates()
    except KeyboardInterrupt:
        print("Program terminated.")
