import cv2
import numpy as np
import pyautogui
import time
from mss import mss
from PIL import Image

bounding_box = {'top': 100, 'left': 0, 'width': 400, 'height': 300}
sct = mss()
def detect_bar_on_screen(image_path):
    # Загружаем целевое изображение для поиска
    target_image = cv2.imread(image_path)
    if target_image is None:
        print("Ошибка: Не удалось загрузить изображение для поиска.")
        return

    # Получаем размеры целевого изображения
    # target_height, target_width = target_image.shape[:2]
    start_point = (5,5)
    end_point = (20,20)
    while True:
        sct_img = sct.grab(bounding_box)
        # Захватываем экран
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Ищем вхождение целевого изображения в текущем кадре
        result = cv2.matchTemplate(frame, target_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.5  # Порог для нахождения совпадения
        locations = np.where(result >= threshold)

        # Если находим совпадение, выводим сообщение в консоль
        if len(locations[0]) > 0:
            print("Изображение bar найдено!")
            cv2.imshow('screen', np.array(sct_img))
            
        #     target_image = cv2.rectangle(target_image, (start_point), (end_point), (0, 255, 0), 2)
        # cv2.imshow("main", target_image) 
            
        # Для отладки: отображаем текущее изображение
        #cv2.imshow('Screen Capture', frame)

        # Прерываем цикл по нажатию клавиши 'q'
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break

    cv2.destroyAllWindows()

# Запуск функции отслеживания
detect_bar_on_screen('objA.png')