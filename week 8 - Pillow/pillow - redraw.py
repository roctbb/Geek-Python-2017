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

        if r < 50 and b < 50 and g < 50:
            pixels[i, j] = (255, 255, 120)

# показываем результат
img.show()

# или сохраняем его в файл
img.save("edited_dog.jpg")