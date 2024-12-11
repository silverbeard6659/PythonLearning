import cv2
import numpy as np
import pyautogui  # Для нажатия кнопок
import mss  # Для захвата экрана
import time  # Для работы с таймером
import keyboard  # Для отслеживания нажатий клавиш

# Функция для нахождения объектов на экране
def find_objects_on_screen(screenshot, template1, template2, threshold1, threshold2):
    # Находим шаблоны на захваченном изображении
    res1 = cv2.matchTemplate(screenshot, template1, cv2.TM_CCOEFF_NORMED)
    res2 = cv2.matchTemplate(screenshot, template2, cv2.TM_CCOEFF_NORMED)

    loc1 = np.where(res1 >= threshold1)
    loc2 = np.where(res2 >= threshold2)

    centers = []

    # Получаем координаты центров первого объекта
    for pt in zip(*loc1[::-1]):  # (x, y) координаты
        cX = pt[0] + template1.shape[1] // 2
        cY = pt[1] + template1.shape[0] // 2
        centers.append((cX, cY))
        break  # Берем только первое найденное соответствие

    # Получаем координаты центров второго объекта
    for pt in zip(*loc2[::-1]):  # (x, y) координаты
        cX = pt[0] + template2.shape[1] // 2
        cY = pt[1] + template2.shape[0] // 2
        centers.append((cX, cY))
        break  # Берем только первое найденное соответствие

    if len(centers) < 2:
        print("Недостаточно объектов для обнаружения!")
        return None

    return centers

# Функция для поиска объекта 3 на экране
def find_object3_on_screen(screenshot, template3, threshold3):
    res = cv2.matchTemplate(screenshot, template3, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold3)

    # Получаем координаты центра объекта 3
    centers = []
    for pt in zip(*loc[::-1]):  # (x, y) координаты
        cX = pt[0] + template3.shape[1] // 2
        cY = pt[1] + template3.shape[0] // 2
        centers.append((cX, cY))
        break  # Берем только первое найденное соответствие

    return centers if centers else None

# Определяем расположение объектов и нажимаем соответствующие кнопки
def determine_position_and_press_buttons(template1_path, template2_path, threshold1=0.8, threshold2=0.8):
    # Загружаем шаблоны объектов
    template1 = cv2.imread(template1_path)
    template2 = cv2.imread(template2_path)

    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Захватываем изображение с первого монитора

        start_time = time.time()  # Запоминаем время начала

        while True:
            # Захватываем изображение с экрана
            screenshot = sct.grab(monitor)
            
            # Конвертируем в BGR формат OpenCV (BGR вместо RGB)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # Находим объекты на экране с заданными threshold
            centers = find_objects_on_screen(img, template1, template2, threshold1, threshold2)

            if centers is None:
                # Проверяем, прошло ли 7 секунд
                if time.time() - start_time >= 7:
                    print("Время попыток истекло. Повторяем...")
                    start_time = time.time()  # Сбрасываем таймер на следующий раунд
                continue  # Если объекты не найдены, продолжаем цикл

            obj1, obj2 = centers
            print(f"Координаты объекта 1: {obj1}, Координаты объекта 2: {obj2}")

            if obj2[0] < obj1[0]:  # Объект2 слева от Объект1
                print("Объект2 слева от Объект1. Нажимаем кнопку 2.")
                pyautogui.press('2')
            else:  # Объект2 справа от Объект1
                print("Объект2 справа от Объект1. Нажимаем кнопку 1.")
                pyautogui.press('1')

# Основная функция для отслеживания и запуска программы
def main(template1_path, template2_path, template3_path, threshold1=0.8, threshold2=0.8, threshold3=0.8):
    while True:
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Захватываем изображение с первого монитора
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # Ищем объект 3 на экране
            if find_object3_on_screen(img, cv2.imread(template3_path), threshold3) is not None:
                print("Объект 3 найден! Нажимаем кнопку 1.")
                pyautogui.press('1')  # Нажимаем кнопку 1
                determine_position_and_press_buttons(template1_path, template2_path, threshold1, threshold2)  # Запускаем основное обнаружение
            else:
                print("Объект 3 не найден. Ожидаем нахождения объекта 3...")

# Пример использования
template1_path = 'objA.png'  # Укажите путь к изображению первого объекта
template2_path = 'objB.png'  # Укажите путь к изображению второго объекта
template3_path = 'obj3.png'  # Укажите путь к изображению объекта 3
threshold1_value = 0.5  # Установите уровень доверия для соответствия первого шаблона
threshold2_value = 0.8  # Установите уровень доверия для соответствия второго шаблона
threshold3_value = 0.8  # Установите уровень доверия для соответствия третьего шаблона

main(template1_path, template2_path, template3_path, threshold1_value, threshold2_value, threshold3_value)