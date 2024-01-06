'''Модуль для запуска обработки видео и фотографий'''
import cv2
import numpy as np


# Функция для обработки фотографии или кадров видео
def handle_frame(image, solve=lambda frame: frame, video_frame=False):
    if not video_frame:
        frame = None
        while True:
            if type(image) is str:
                frame = cv2.imread(image).copy()
            elif type(image) is np.ndarray:
                frame = image.copy()
                
            result = solve(frame)
            cv2.imshow("Result", result)
	
            k = cv2.waitKey(10) & 0xFF
            if (k == ord('q')):
                break

    else:
        frame = image
        result = solve(frame)
        return result

# Функция для обработки видео покадрово. Принимает на вход видео(или камеру) и функцию для решения заданной задачи
def handle_video(video_capture: str | int, solve=lambda frame: frame):
    cap = cv2.VideoCapture(video_capture)
    while True:
        _, frame = cap.read()
        
        if frame is not None:
            result = handle_frame(image=frame, solve=solve, video_frame=True)
        else:
            break

        cv2.imshow("Result", result)
	
        k = cv2.waitKey(10) & 0xFF
        if (k == ord('q')):
            break