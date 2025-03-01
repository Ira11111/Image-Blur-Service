import os
import uuid
from io import BytesIO
from typing import List, Tuple

from PIL import Image, ImageFilter


def process_images(images: List) -> Tuple[List, str]:
    """
    Функция создает массив, где в каждом элементе находятся:
    - содержимое файла
    - название файла
    - название директории, в которую будет сохранено обработанное изображение
    """
    image_buffers = []
    for image in images:
        buf = BytesIO(image.read())
        image_buffers.append(buf)

    dir_name = os.path.join("orders", str(uuid.uuid4()))
    os.makedirs(dir_name, exist_ok=True)
    image_data = [
        (image_buf.getvalue(), image.filename, dir_name)
        for image_buf, image in zip(image_buffers, images)
    ]
    return image_data, dir_name


def blur_image(image_bytes: bytes, image_name: str, path: str) -> None:
    """
    Функция принимает на вход имя входного и выходного файлов.
    Применяет размытие по Гауссу со значением 5.
    """
    with Image.open(BytesIO(image_bytes)) as img:
        img.load()
        new_img = img.filter(ImageFilter.GaussianBlur(5))

        with open(f"{path}/blur_{image_name}", "wb") as output:
            new_img.save(output)
