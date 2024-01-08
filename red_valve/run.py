import os
from pathlib import Path

from config import IMAGES_DIR
from cv_utils import handle_frame, handle_video
from .red_valve_task import red_valve_task_handle_old, red_valve_task_handle


def run(method=red_valve_task_handle_old, image_file=None, video_file=None, image_files=[],  *args, **kwargs):
    try:
        if image_file:
            handle_frame(image=image_file, solve=method)
        if video_file:
            handle_video(video=video_file, solve=method)
        if len(image_files):
            handle_frame(images=image_files, solve=method)
    except Exception as e:
        print(e)
    
    return "Завершение просмотра..."
