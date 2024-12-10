import cv2
import numpy as np
import pyautogui
import time

def detect_init_on_screen(image_path):
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
        threshold = 0.8  # Порог для нахождения совпадения
        locations = np.where(result >= threshold)

        # Если находим совпадение, выводим сообщение в консоль
        if len(locations[0]) > 0:
            print("Изображение найдено!")
            pyautogui.press('1')  # Нажимаем кнопку '1'
            break

# Запуск функции отслеживания
detect_init_on_screen('geeks14.png')

cv2.destroyAllWindows()