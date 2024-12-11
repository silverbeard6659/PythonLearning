import cv2
import numpy as np
import pyautogui  # Для нажатия кнопок
import mss  # Для захвата экрана
import time  # Для работы с таймером
import keyboard  # Для отслеживания нажатий клавиш

def main(template1_path, template2_path, template3_path, threshold1=0.8, threshold2=0.8, threshold3=0.8):
    while True:
        with mss.mss() as sct:
            monitor = sct.monitors[0]  # Захватываем изображение с первого монитора
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            pyautogui.press('1')  # Нажимаем кнопку 1

            # Ищем объект 3 на экране
            if find_object3_on_screen(img, cv2.imread(template3_path), threshold3) is not None:
                print("Объект 3 найден! Нажимаем кнопку 1.")
                pyautogui.press('1')  # Нажимаем кнопку 1
                determine_position_and_press_buttons(template1_path, template2_path, threshold1, threshold2)  # Запускаем основное обнаружение
            else:
                print("Объект 3 не найден. Ожидаем нахождения объекта 3...")