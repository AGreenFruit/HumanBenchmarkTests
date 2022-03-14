import numpy as np
import cv2
from mss import mss
# import time
import pyautogui

def main():
	width, height = pyautogui.size()
	bounding_box = {'top': 0, 'left': 0, 'width': width, 'height': height}
	sct = mss()

	# Find region with blue and create bounding box from that
	sct_img = sct.grab(bounding_box)
	img = np.array(sct_img)

	# Image Grayscale/Processing
	im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	im = cv2.GaussianBlur(im, (5,5), 0)
	im = cv2.Canny(im, threshold1=180, threshold2=255)

	lines = cv2.HoughLines(im,1,np.pi/180,300)

	point = 0
	if lines is not None and len(lines) > 1:
		# for i in range(len(lines)):
		for i in range(0,2):
			rho = lines[i][0][0]
			theta = lines[i][0][1]
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))
			if i == 0:
				point = y1


	# Initilizes blue and red colors as well as the first bounding box
	bounding_box = {'top': point-100, 'left': 0, 'width': 10, 'height': 10}
	sct_img = sct.grab(bounding_box)
	im = np.array(sct_img)



	blue = im[0][0][0]
	pyautogui.click(0,point-100)
	sct_img = sct.grab(bounding_box)
	im = np.array(sct_img)
	red = im[0][0][0]

	counter = 0
	while True:
		sct_img = sct.grab(bounding_box)
		im = np.array(sct_img)
		if im[0][0][0] != red:
			pyautogui.click(0,point-100)
			counter += 1
		if counter == 10:
			break;
main() 