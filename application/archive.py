import os.path
import shutil
import zipfile

"""
Здесь описана логика создания байтового буфера архива обработанных изображений
"""


def create_archive(path):
    arc_name = f"{path[2:]}.zip"
    if not os.path.exists(arc_name):
        if os.path.exists(path):
            with zipfile.ZipFile(arc_name, "w", zipfile.ZIP_DEFLATED) as zipf:
                for image in os.listdir(path):
                    image_path = os.path.join(path, image)
                    zipf.write(image_path)
            shutil.rmtree(path)
        else:
            return

    return arc_name
