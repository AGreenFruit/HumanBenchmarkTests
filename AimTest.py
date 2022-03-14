import numpy as np
import cv2
from mss import mss
from PIL import Image
import time
import pyautogui

def process_img(original_image):
	processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)


	circles = cv2.HoughCircles(processed_img, 
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
               param2 = 35, minRadius = 20, maxRadius = 60)
  
	if circles is not None:
		circles = np.uint16(np.around(circles))
		for pt in circles[0, :]:
			a, b, r = pt[0], pt[1], pt[2]
			pyautogui.click(a, b)
	return processed_img

def main():
	bounding_box = {'top': 0, 'left': 0, 'width': 1500, 'height': 600} #Get dimensions of screen

	sct = mss()

	while True:
		sct_img = sct.grab(bounding_box)
		#cv2.imshow('screen2', process_img(np.array(sct_img)))
		process_img(np.array(sct_img))
		if (cv2.waitKey(1) & 0xFF) == ord('q'):
			cv2.destroyAllWindows()
			break
main() 