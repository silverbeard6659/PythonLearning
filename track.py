import cv2
import numpy as np

def detect_object(image_path, lower_color=np.array([110, 50, 50]), upper_color=np.array([130, 255, 255])):
    # Загружаем изображение
    image_path = 'scr1.png'
    image = cv2.imread(image_path)
    if image is None:
        print("Ошибка: Не удалось загрузить изображение.")
        return None

    # Конвертируем изображение в цветовую модель HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Создаем маску по нижнему и верхнему пределам заданного цвета
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Находим контуры объектов на маске
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Проверяем, найдены ли контуры
    if contours:
        # Находим самый большой контур (предполагая, что это наш объект)
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Рисуем прямоугольник вокруг объекта
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Отображаем кадр с отмеченным объектом
        cv2.imshow('Detected Object', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Возвращаем координаты объекта
        return (x, y, w, h)
    else:
        print("Объект не найден.")
        return None

# Пример вызова функции
coordinates = detect_object('path_to_your_image.jpg')
if coordinates:
    print(f"Координаты объекта: {coordinates}")