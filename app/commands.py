import shutil
from pathlib import Path

from .files_utils import *
from config import *
from cv_utils import handle_video, handle_frame
from red_valve import run


def _check_type(filename):
    videos = ["mp4"]
    images = ["png"]
    ext = str(filename).split('.')[-1]
    if ext in videos:
        return "video"
    elif ext in images:
        return "image"
    return None

def custom_video():
    global CUSTOM_VIDEO_PATH, VIDEOS_DIR, LINK_CUSTOM_ZIP

    if not check_files(file_path=CUSTOM_VIDEO_PATH):
        download_unpack(LINK_CUSTOM_ZIP, path=VIDEOS_DIR)

    result = run(video_file=str(CUSTOM_VIDEO_PATH))
    return result
    

def crop1_mp4():
    global CROP1_VIDEO_PATH, LINK_VIDEOS_ZIP, VIDEOS_DIR

    if not check_files(file_path=CROP1_VIDEO_PATH):
        download_unpack(LINK_VIDEOS_ZIP, path=VIDEOS_DIR)

    result = run(video_file=str(CROP1_VIDEO_PATH))
    return result
    

def crop2_mp4():
    global CROP2_VIDEO_PATH, LINK_VIDEOS_ZIP, VIDEOS_DIR

    if not check_files(file_path=CROP2_VIDEO_PATH):
        download_unpack(LINK_VIDEOS_ZIP, path=VIDEOS_DIR)

    result = run(video_file=str(CROP2_VIDEO_PATH))
    return result
    

def control_pictures():
    global IMAGES_DIR, LINK_IMAGES_ZIP

    if not check_files(files_path=IMAGES_DIR):
        download_unpack(LINK_IMAGES_ZIP, path=IMAGES_DIR)

    result = run(image_files=path_array(IMAGES_DIR, string=True))
    return result

    
def open_file():
    global VIDEOS_DIR, IMAGES_DIR

    filename = input("Укажите имя файла, который надо открыть\n>")
    filename_obj = Path(filename)
    file_path = None
    file_type = _check_type(filename_obj)
    if file_type == "video":
        file_path = str(Path(VIDEOS_DIR, filename_obj))
    elif file_type == "image":
        file_path = str(Path(IMAGES_DIR, filename_obj))

    result = None
    if check_files(file_path=file_path):
        file_type = _check_type(file_path)
        if file_type == "video":
            result = run(video_file=file_path)
        elif file_type == "image":
            result = run(image_file=file_path)

    else:
        return "Файл не найден в папках videos или images.\nПопробуйте установить специальной командой"
        
    if result:
        return result
    
    return "Завершение подпрограммы..."


def input_google_link():
    global VIDEOS_DIR, IMAGES_DIR, GOOGLE_DRIVE_LINK

    temp_dir = Path("Temp")
    id = input("Укажите id ZIP-файла на Google Drive\n>")
    download_unpack(GOOGLE_DRIVE_LINK.format(id), temp_dir)
    check_temp(temp_dir)
    for filename_obj in path_array(temp_dir):
        file_type = _check_type(filename_obj)
        if file_type == "video":
            move_file_to_dir(filename_obj, VIDEOS_DIR)
        elif file_type ==  "image":
            move_file_to_dir(filename_obj, IMAGES_DIR)

    delete_file(temp_dir)
    return "Загрузка завершена."


commands = {
    "1. Запустить обрезанное видео": custom_video,
    "2. Запустить crop1.mp4": crop1_mp4,
    "3. Запустить crop2.mp4": crop2_mp4,
    "4. Проверить на контрольных изображениях": control_pictures,
    "5. Указать путь к файлу для одиночной проверки": open_file,
    "6. Указать id ZIP-файла на Google Drive для скачивания": input_google_link,
}