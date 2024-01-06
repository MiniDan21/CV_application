import math

import cv2 
import numpy as np


def laplacian(frame, ddepth=cv2.CV_8U, kernel_size=5):
	return cv2.Laplacian(frame, ddepth, ksize=kernel_size)

# Константа, определяющая допустимую разницу для лямбда-функции diff
DIFF_NUM = 10
# Переменная для запоминания предыдущей окружности
prev_circle = None
# Переменная для построения предыдущих лучей
prev_point2 = None
# Вспомогательная функция, чтобы окружность не дергалась - определяет разницу радиусов и координат центра предыдущей и новой окружностей
diff = lambda c1, c2: abs(c1[0] - c2[0]) > DIFF_NUM or abs(c1[1] - c2[1]) > DIFF_NUM or abs(c1[2] - c2[2]) > DIFF_NUM

# Посчитать длину отрезка по двум точкам
dist = lambda p1, p2: ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

# Функция для рисования окружности со сравнением предыдущей окружности и переданной
def draw_circle(frame, circle, color=(255, 255, 0), thickness=1):
	global prev_circle, prev_point2
	if prev_circle is None:
		prev_circle = circle
	else:
	# Если разница больше DIFF_NUM, то обновить предыдущую окружность
		if diff(np.int16(prev_circle), np.int16(circle)):
			prev_circle = circle
		else:
			circle = prev_circle
	center =  circle[0], circle[1]
	radius = circle[2]

	cv2.circle(frame, center, radius, color, thickness)
	# if prev_point2 is not None:
	# 	draw_line(frame, center, prev_point2)

def skelezation(img):
	size = np.size(img)
	skel = np.zeros(img.shape,np.uint8)

	ret,img = cv2.threshold(img,127,255,0)
	element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
	done = False

	while(not done):
		eroded = cv2.erode(img,element)
		temp = cv2.dilate(eroded,element)
		temp = cv2.subtract(img,temp)
		skel = cv2.bitwise_or(skel,temp)
		img = eroded.copy()

		zeros = size - cv2.countNonZero(img)
		if zeros==size:
			done = True

	return skel

def cut_by_circle(frame, circle=None, diff=25, center_diff=0, spec_cut=False):
	canvas = np.zeros_like(frame, dtype=frame.dtype)
	global prev_circle
	if prev_circle is not None:
		circle = prev_circle
	if circle is not None:
		x = circle[0]
		y = circle[1]
		r = circle[2]
		one = y - r + diff
		two = y + r - diff
		three = x - r + diff
		four = x + r - diff
		# Специальное обрезание половины для подсчета угла наклона
		if spec_cut:
			fragment = frame[:, x:four]
			canvas[:, x:four] = fragment
		else:
			fragment = frame[one:two, three:four]
			canvas[one:two, three:four] = fragment
		# Вырезать центр, если понадобится
		canvas[y-center_diff:y+center_diff,x-center_diff: x+center_diff] = 0
	return canvas

# Функция для определения максимально удаленных точек в каждом квадранте
def max_distance(center_point=None, points=[]):
	global prev_circle
	max_dist = (0, None)


	if prev_circle is not None:
		center_point = (prev_circle[0], prev_circle[1])
	if center_point is not None:
		for point in points:
			d = dist(center_point, point[0])
			if d > max_dist[0]:
				max_dist = (d, point[0])

	return max_dist[1]


# DIFF_LINE_NUM = 10
# Потенциально вспомогательная функция, чтобы линии не дергались
# diff_line = lambda d1, d2: abs(d1[2] - d2[2]) > DIFF_LINE_NUM or abs(d1[3] - d2[3]) > DIFF_LINE_NUM  
DIFF_ARC_MIN_NUM = 0  # чтобы зафиксировать поворот
# Вспомогательная функция, чтобы линия не дергалась
diff_arc = lambda arc1, arc2: DIFF_ARC_MIN_NUM < abs(arc2 - arc1)
# Определить угол между двумя точками в радианах
arc = lambda p1, p2: math.atan((p2[1] - p1[1])/(p2[0] - p1[0]))
# Поворот точки на 120 градусов
rotate_120 = lambda c, p: np.int16(np.round((
		(p[0] - c[0])*math.cos(np.pi * 120 / 180) - (p[1] - c[1])*math.sin(np.pi * 120 / 180) + c[0], 
		(p[0] - c[0])*math.sin(np.pi * 120 / 180) + (p[1] - c[1])*math.cos(np.pi * 120 / 180) + c[1],
	)))

ray = lambda c, p: (1000*(p[0] - c[0]) + c[0], 1000*(p[1] - c[1]) + c[1])

def count_degree(point1, point2):
	new_arc = 90
	# Если точка не под центром находится, то пересчитать угол
	if point1[0] != point2[0]:
		new_arc = 180*arc(point1, point2)/np.pi		
		if point1[0] > point2[0] and point1[1] > point2[1]:
			new_arc += 60
			if new_arc > 120:
				new_arc -= 120
		elif point1[0] < point2[0] and point1[1] > point2[1]:
			new_arc = 120 + new_arc
		elif point1[0] > point2[0] and point1[1] < point2[1]:
			new_arc += 60
			if new_arc < 0:
				new_arc += 120
		
		if new_arc < 0 or new_arc > 120:
			print(point1, point2)
	return new_arc

def draw_line(frame, point1=None, point2=None):
	global prev_circle, prev_point2

	if prev_circle is None:
		return
	else:
		point1 = (prev_circle[0], prev_circle[1])

	if point1 is not None and point2 is not None:
		if prev_point2 is not None:
			if abs(count_degree(point1, point2) - count_degree(point1, prev_point2)) > DIFF_ARC_MIN_NUM:
				prev_point2 = point2
			else:
				point2 = prev_point2
		else:
			prev_point2 = point2

		cv2.line(frame, ray(point1, point2), point1, (0,255,0), 1, cv2.LINE_AA)
		second_point = rotate_120(point1, point2)
		cv2.line(frame, ray(point1, second_point), point1, (0,255,0), 1, cv2.LINE_AA)
		third_point = rotate_120(point1, second_point)
		cv2.line(frame, ray(point1, third_point), point1, (0,255,0), 1, cv2.LINE_AA)

		new_arc = count_degree(point1, point2)
		cv2.putText(frame, str(round(new_arc)), (0, 12), 
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 2, 2)
