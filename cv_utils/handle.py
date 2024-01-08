'''Модуль для запуска обработки видео или изображения'''
import cv2
import numpy as np


# Функция для обработки фотографии или кадров видео
def handle_frame(image=None, solve=lambda frame: frame, video_frame=False, images=[]):
    if not video_frame:
        frame = None
        if image is not None:
            if type(image) is str:
                frame = cv2.imread(image).copy()
            elif type(image) is np.ndarray:
                frame = image.copy()
            result = solve(frame)
            window_name = "Result"
            cv2.imshow(window_name, result)
            # cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
            while True:        
                result = solve(frame)
                window_name = "Result"
                cv2.imshow(window_name, result)
                k = cv2.waitKey(10) & 0xFF
                if (k == ord('q')):
                    break
        elif len(images):
            results = []
            for image in images:
                if type(image) is str:
                    frame = cv2.imread(image).copy()
                elif type(image) is np.ndarray:
                    frame = image.copy()
                results.append((image, solve(frame)))
            
            for image, result in results:
                cv2.imshow(image, result)
                # cv2.setWindowProperty(image, cv2.WND_PROP_TOPMOST, 1)
            while True:
                k = cv2.waitKey(10) & 0xFF
                if (k == ord('q')):
                    break

    else:
        frame = image
        result = solve(frame)
        return result

    cv2.destroyAllWindows()

# Функция для обработки видео покадрово. Принимает на вход видео(или камеру) и функцию для решения заданной задачи
def handle_video(video: str | int, solve=lambda frame: frame):
    cap = cv2.VideoCapture(video)
    while True:
        _, frame = cap.read()
        
        if frame is not None:
            result = handle_frame(image=frame, solve=solve, video_frame=True)
        else:
            break

        window_name = "Result"
        cv2.imshow(window_name, result)
        # cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
	
        k = cv2.waitKey(10) & 0xFF
        if (k == ord('q')):
            break
    cap.release()
    cv2.destroyAllWindows()