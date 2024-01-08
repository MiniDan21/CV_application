import os
import shutil
from pathlib import Path
import zipfile
from tqdm.auto import tqdm

import gdown


def _download_zip(zip_link, path):
    try:
        gdown.download(zip_link, path)
    except KeyboardInterrupt:
        print("Отмена загрузки...")

def delete_file(file_path):
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    else:
        os.remove(file_path)

def move_file_to_dir(file_path: Path, dir_path: Path) -> bool:
    if not dir_path.exists():
        os.mkdir(dir_path)
    if file_path.exists():
        shutil.move(file_path, Path(dir_path, file_path.name))
        return True
    return False

def extract_zip(zip_path, extract_path=None):
    with zipfile.ZipFile(zip_path) as zip_file:
        # Извлекаем все файлы из папок в архиве
        for file in zip_file.namelist():
            file_obj = Path(file)
            if not file_obj.is_dir():
                try:
                    os.mkdir("TEMP")
                except Exception:
                    pass
                zip_file.extract(str(file), Path("TEMP"))
                move_file_to_dir(Path("TEMP", file_obj), extract_path)
                delete_file("TEMP")

def _parent(file: Path):
    return file.parent

def check_type(filename):
    videos = ["mp4", "mov", "wmv", "avi", "avchd", "webm", "flv", "mkv", "f4v", "swf", "gif"]
    images = ["png", "jpeg", "jpg", "pict", "pct", "webp", "jp2"]
    ext = str(filename).split('.')[-1]
    if ext in videos:
        return "video"
    elif ext in images:
        return "image"
    return None

def path_array(dir, string=False):
    files = []
    for file_name in os.listdir(dir):
        file_path = Path(dir, file_name)
        if string:
            file_path = str(file_path)
        files.append(file_path)
    return files

def download_unpack(zip_link, path):
    if not os.path.exists(path):
        os.mkdir(path)
    _download_zip(zip_link, "temp.zip")
    extract_zip("temp.zip", path)
    delete_file("temp.zip")
    


def check_files(file_path=None, dir_path=None, files_path=None) -> bool:
    '''Проверить наличие файла по пути или наличие директории и файлов внутри'''
    file_ex  = False
    dir_ex   = False
    files_ex = False
    if file_path:
        file_ex = os.path.exists(file_path)
    if dir_path:
        dir_ex = os.path.exists(dir_path)
    if files_path:
        if os.path.exists(files_path):
            if len(os.listdir(files_path)):
                files_ex = True

    return any((file_ex, dir_ex, files_ex))

def check_temp(temp_path):
    '''Вспомогательная функция, чтобы создать temp, если нет'''
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)