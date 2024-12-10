import cv2
import numpy as np
import pyautogui
import time

def detect_bar_on_screen(image_path):
    # Загружаем целевое изображение для поиска
    target_image = cv2.imread(image_path)
    if target_image is None:
        print("Ошибка: Не удалось загрузить изображение для поиска.")
        return

    # Получаем размеры целевого изображения
    target_height, target_width = target_image.shape[:2]

    while True:
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
            print("Изображение найдено!")
            
        # Для отладки: отображаем текущее изображение
        #cv2.imshow('Screen Capture', frame)

        # Прерываем цикл по нажатию клавиши 'q'
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break

    cv2.destroyAllWindows()

# Запуск функции отслеживания
detect_bar_on_screen('objA.png')