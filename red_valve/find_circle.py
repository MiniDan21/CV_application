import cv2
import numpy as np
from skimage.transform import hough_circle_peaks, hough_circle


def find_circle(frame):
	circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 2, 100, param1=106, param2=17, minRadius=54, maxRadius=56)
	if circles is not None:
		circles = np.uint16(np.around(circles))
		for circle in circles[0, :]:
			return circle

	# hough_rad = np.arange(54, 55)
	# hough_res = hough_circle(frame, hough_rad)
	# res = hough_circle_peaks(np.uint16(np.around(hough_res)), hough_rad, total_num_peaks=1)
	# if len(res[0]):
	# 	a, cx, cy, rad = res
	# 	return (cx[0], cy[0], rad[0])
