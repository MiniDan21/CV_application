import cv2
import numpy as np
from skimage.morphology import convex_hull_image, skeletonize, thin, medial_axis
from skimage.transform import hough_circle, hough_circle_peaks

import cv_utils
from .find_circle import find_circle


kernel = None
sliders = False
done = False
sliderName = "Sliders"

# Небольшая функция для демонстрации явного изменения kernel
def change_kernel(k_size):
    global kernel
    kernel = np.ones((k_size, k_size), np.uint8)

def red_new(frame, handles=False, sliders_on=False, lab=False, bgr=False):
    global sliders, sliderName
    color_space = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if bgr:
        color_space = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    elif lab:
        color_space = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        color_space = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    result = np.zeros_like(color_space, dtype=color_space.dtype)
    # Для обработки вентиля
    if sliders_on:
        if done:
            h = cv2.getTrackbarPos('h', sliderName)
            s = cv2.getTrackbarPos('s', sliderName)
            v = cv2.getTrackbarPos('v', sliderName)
            u_h = cv2.getTrackbarPos('u_h', sliderName)
            u_s = max(s, cv2.getTrackbarPos('u_s', sliderName))
            u_v = max(v, cv2.getTrackbarPos('u_v', sliderName))
            mask = cv2.inRange(color_space, (h, s, v), (u_h, u_s, u_v))
            # add_mask = cv2.inRange(hsv, (0, 29, 0), (85, 138, 120))
            result = cv2.bitwise_or(mask, mask)	
        else:
            sliders = True
    elif lab:
        min_lab = (38, 132, 113) 
        max_lab = (255, 163, 141)
        mask = cv2.inRange(color_space, min_lab, max_lab)
        # add_mask = cv2.inRange(hsv, (0, 29, 0), (85, 138, 120))
        result = cv2.bitwise_or(mask, mask)	
    elif not handles:
        # min_val = (141, 25, 54)
        # max_val = (180, 150, 160)
        min_val = (90, 40, 0) 
        max_val = (150, 150, 150)
        # Фильтрация по красному цвету 
        mask = cv2.inRange(color_space, min_val, max_val)
        # Дополнительная маска, для дополнения диапазона красного цвета
        # add_mask = cv2.inRange(color_space, (0, 29, 0), (85, 138, 120))
        result = cv2.bitwise_or(mask, mask)	
    # Для обработки ручек
    else:
        min_val = (160, 70, 30)
        max_val = (180, 170, 120)
        # Фильтрация по красному цвету 
        mask = cv2.inRange(color_space, min_val, max_val)
        result = mask
    return result

def red(frame, handles=False):
    color_space = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    result = np.zeros_like(color_space, dtype=color_space.dtype)
    # Для обработки вентиля
    if not handles:
        min_val = (141, 25, 54)
        max_val = (180, 150, 160)
        # Фильтрация по красному цвету 
        mask = cv2.inRange(color_space, min_val, max_val)
        # Дополнительная маска, для дополнения диапазона красного цвета
        add_mask = cv2.inRange(color_space, (0, 29, 0), (85, 138, 120))
        result = cv2.bitwise_or(mask, add_mask)	
    # Для обработки ручек
    else:
        min_val = (160, 70, 30)
        max_val = (180, 170, 120)
        # Фильтрация по красному цвету 
        mask = cv2.inRange(color_space, min_val, max_val)
        result = mask
    return result

def red_valve_task_handle_old(frame):
# Опциональные обработки ---------------------{

    blur = cv2.GaussianBlur(frame, (3, 3), 0)

# }--------------------------------------------


# Фильтр по красному -------------------------{
    
    red_mask = red(blur)
    cv2.imshow("mask", red_mask)
# }--------------------------------------------


# Определение круга вентиля ------------------{
    
    # Если круг плохо определяется, можно поменять размер ядра для erode
    change_kernel(3)
    eroded = cv2.erode(red_mask, kernel, iterations=1)
    opened = cv2.morphologyEx(eroded, cv2.MORPH_OPEN, kernel)
    circle = find_circle(opened)
    center_point = None
    if circle is not None:
        center_point = (circle[0], circle[1])
        cv_utils.draw_circle(frame=frame, circle=circle)

# }--------------------------------------------


# Определение ручек вентиля ------------------{
    red_mask = red(blur, handles=True)
    cut = cv_utils.cut_by_circle(red_mask, circle=circle)
    eroded = cv2.erode(cut, kernel, iterations=2)   
    contours, hierarchy = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # cv2.drawContours(frame, contours, 0, (255,0,0), 1)
    if len(contours):
        contour = contours[0]
        max_dist_point = cv_utils.max_distance(center_point=center_point, points=contour)
        cv_utils.draw_line(frame, center_point, max_dist_point)
    result = frame

# }--------------------------------------------

    return result


def red_valve_task_handle(frame):
    global sliders, done, sliderName

# Опциональные обработки ---------------------{

    blur = cv2.GaussianBlur(frame, (5, 5), 0)
    # КОСТЫЛЬ, КОТОРЫЙ НАДО УБРАТЬ ПОСЛЕ ТЕСТИРОВАНИЯ
    if sliders and not done:
        done = True
        cv2.namedWindow(sliderName)
        cv2.createTrackbar('h', sliderName, 95, 255, lambda v: v)
        cv2.createTrackbar('s', sliderName, 105, 255, lambda v: v)
        cv2.createTrackbar('v', sliderName, 0, 255, lambda v: v)
        cv2.createTrackbar('u_h', sliderName, 150, 255, lambda v: v)
        cv2.createTrackbar('u_s', sliderName, 255, 255, lambda v: v)
        cv2.createTrackbar('u_v', sliderName, 205, 255, lambda v: v)

# }--------------------------------------------


# Фильтр по красному -------------------------{
    
    # hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # hsv: (95, 105, 0) (150, 255, 205)
    # clahe_res = cv_utils.clahe(hsv, first=False, clipLimit=10.0)
    result = red(cv2.cvtColor(blur, cv2.COLOR_BGR2RGB))
    
# }--------------------------------------------


# Определение круга вентиля ------------------{
    # (38, 132, 113) (255, 163, 141)
    # # Плохо определяет круг на vlcsnap-2020-07-08-09h36m29s510.png
    # # Если круг плохо определяется, можно поменять размер ядра для erode
    # change_kernel(3)
    # eroded = cv2.erode(red_mask, kernel, iterations=2)
    # # # med_axis = np.where(medial_axis(eroded), np.uint8(255), np.uint8(0))
    # change_kernel(3)
    # opened = cv2.morphologyEx(eroded, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("TEST", eroded)
    # cv2.imshow("Opened", opened)
    # circle = find_circle(eroded)
    # center_point = None
    # if circle is not None:
    #     cv_utils.draw_circle(frame=frame, circle=circle)

# }--------------------------------------------


# Определение ручек вентиля ------------------{

# }--------------------------------------------

    return result