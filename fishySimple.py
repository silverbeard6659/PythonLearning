import cv2
import numpy as np
import pyautogui  # Для нажатия кнопок
import mss  # Для захвата экрана
import time  # Для работы с таймером
import keyboard  # Для отслеживания нажатий клавиш

OBJECT_3 = ('obj3.png')
threshold3 = 0.8
OBJECT_A = ('objA.png')
OBJECT_B = ('objB.png')
def find_object3_on_screen(screenshot, template, threshold):
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    # Если объект найден, возвращаем True
    return loc[0].size > 0

while True:
    print('starting fishing, wait 3 sec for start')
    time.sleep(3) # waiting for new cycle
    print('starting now')
    keyboard.press('1')
    while True:
        with mss.mss() as sct:
            monitor = sct.monitors[0]  # Захватываем изображение с первого монитора
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # Ищем объект 3 на экране
            if find_object3_on_screen(img, cv2.imread(OBJECT_3), threshold3) is not None:
                print("Объект 3 найден! Нажимаем кнопку 1.")
                pyautogui.press('1')  # Нажимаем кнопку 1
                print('button pressed go next step')
                #determine_position_and_press_buttons(template1_path, template2_path, threshold1, threshold2)  # Запускаем основное обнаружение
            else:
                print("Объект 3 не найден. Ожидаем нахождения объекта 3...")
    
    if keyboard.is_pressed('q'):
        print('ending')
        break # end if Q pressed