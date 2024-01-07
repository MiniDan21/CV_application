import os
from pathlib import Path
from time import sleep

from config import IMAGES_DIR
from cv_utils import handle_frame, handle_video
from .solve import rev_valve_task


def run(method=rev_valve_task, image_file=None, video_file=None, image_files=[],  *args, **kwargs):
    if image_file:
        handle_frame(image=image_file, solve=method)
    if video_file:
        handle_video(video=video_file, solve=method)
    if len(image_files):
        handle_frame(images=image_files)
    
    # Костыль, который решает проблему с незакрытием окон
    exit(0)
    return "Hello, world!"
