import shutil
from pathlib import Path

from .files_utils import *
from cv_utils import handle_video, handle_frame
from red_valve import solve


ZIP_DIR           = Path("zip")
VIDEOS_DIR        = Path("videos")
VIDEOS_ZIP_DIR    = Path(ZIP_DIR, VIDEOS_DIR)
IMAGES_DIR        = Path("images")
IMAGES_ZIP_DIR    = Path(ZIP_DIR, IMAGES_DIR)

# Можно записать в массив при помощи _path_array
CUSTOM_VIDEO_PATH = Path(VIDEOS_DIR, "crop3.mp4")
CROP1_VIDEO_PATH  = Path(VIDEOS_DIR, "crop1.mp4")
CROP2_VIDEO_PATH  = Path(VIDEOS_DIR, "crop2.mp4")

GOOGLE_DRIVE_LINK = "https://drive.google.com/uc?id={0}"
LINK_CUSTOM_ZIP   = GOOGLE_DRIVE_LINK.format("1orsUuSHidM9-aHLWZvJQsjcr9zHMiadg")
LINK_VIDEOS_ZIP   = GOOGLE_DRIVE_LINK.format("12ZTjcM-YhjACSPYsJF1QGP6m9IxyYPWq")
LINK_IMAGES_ZIP   = GOOGLE_DRIVE_LINK.format("1FlmfAu7MaUQ4Mb0-IShb9XiLFCqJs0xB")
    

def custom_video():
    global CUSTOM_VIDEO_PATH, VIDEOS_DIR, LINK_CUSTOM_ZIP
    if not check_files(file_path=CUSTOM_VIDEO_PATH):
        # try:
        #     id = input("Файл не найден. Укажите id ZIP-файла на Google Drive\n>")
        # except KeyboardInterrupt:
        #     return f"\nНе удалось загрузить"
        download_unpack(LINK_CUSTOM_ZIP, path=VIDEOS_DIR)

    result = solve(video_path=CUSTOM_VIDEO_PATH)
    # if result:
    return result
    
def crop1_mp4():
    global CROP1_VIDEO_PATH, LINK_VIDEOS_ZIP, VIDEOS_DIR
    if not check_files(file_path=CROP1_VIDEO_PATH):
        download_unpack(LINK_VIDEOS_ZIP, path=VIDEOS_DIR)
    result = solve(video_path=CROP1_VIDEO_PATH)
    if result:
        return result
    
def crop2_mp4():
    global CROP2_VIDEO_PATH, LINK_VIDEOS_ZIP, VIDEOS_DIR
    if not check_files(file_path=CROP2_VIDEO_PATH):
        download_unpack(LINK_VIDEOS_ZIP, path=VIDEOS_DIR)
    result = solve(video_path=CROP2_VIDEO_PATH)
    if result:
        return result
    
def control_pictures():
    global IMAGES_DIR, LINK_IMAGES_ZIP
    try:
        if not check_files(files_path=IMAGES_DIR):
            download_unpack(LINK_IMAGES_ZIP, path=IMAGES_DIR)
        result = solve(images_path=path_array(IMAGES_DIR))
        if result:
            return result
    except Exception as e:
        return e
    
def input_google_link():
    global VIDEOS_DIR, IMAGES_DIR, GOOGLE_DRIVE_LINK
    temp_dir = Path("Temp")
    try:
        id = input("Укажите id ZIP-файла на Google Drive\n>")
    except KeyboardInterrupt:
        return "Возврат в меню."
    download_unpack(GOOGLE_DRIVE_LINK.format(id), temp_dir)
    try:
        check_temp(temp_dir)
        for file in path_array(temp_dir):
            print(file)
            if file.suffix == ".mp4":
                move_file_to_dir(file, VIDEOS_DIR)
            elif file.suffix == ".png":
                move_file_to_dir(file, IMAGES_DIR)
        delete_file(temp_dir)
    except Exception as e:
        return e
    return "Загрузка завершена."


commands = {
    "1. Запустить обрезанное видео": custom_video,
    "2. Запустить crop1.mp4": crop1_mp4,
    "3. Запустить crop2.mp4": crop2_mp4,
    "4. Проверить на контрольных фотографиях": control_pictures,
    "5. Указать id ZIP-файла на Google Drive для скачивания": input_google_link,
    "6. Указать путь к файлу для одиночной проверки": lambda x: True,
}