import numpy as np
import cv2
from mss import mss
from PIL import Image
import time
import pyautogui

def main():
	bounding_box = {'top': 150, 'left': 0, 'width': 500, 'height': 300} #Get dimensions of screen

	sct = mss()

	while True:
		# time.sleep(1)
		sct_img = sct.grab(bounding_box)
		FImg = np.array(sct_img)
		pixel = FImg[0][0][0]
		# print(pixel)
		if pixel == 209:
			# print("Blue")
			pyautogui.click(150,150)
		elif pixel == 106:
			# print("Green")
			pyautogui.click(150,150)
		# else:
		# 	print("Red")
		#cv2.imshow('screen2', process_img(np.array(sct_img)))
		# process_img(np.array(sct_img))
		if (cv2.waitKey(1) & 0xFF) == ord('q'):
			cv2.destroyAllWindows()
			break
main() 