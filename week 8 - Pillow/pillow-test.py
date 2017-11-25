# импортируем библиотеку
from PIL import Image

# открываем файл
img = Image.open("dog.jpg")

# загружаем матрицу пикселей
pixels = img.load()

# цикл по всем пикселям
# img.width - ширина картинки
# img.height - высота картинки
for i in range(img.width):
    for j in range(img.height):
        # получаем цвет
        r, g, b = pixels[i, j]

        b = b + 150
        if b > 255:
            b = 255

        # сохраняем пиксель обратно
        pixels[i, j] = (r, g, b)

# показываем результат
img.show()

# или сохраняем его в файл
img.save("edited_dog.jpg")