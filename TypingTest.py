import pytesseract
import numpy as np
import cv2
from mss import mss
import pyautogui
import time


def main():
	width, height = pyautogui.size()
	bounding_box = {'top': 0, 'left': 0, 'width': width, 'height': height}
	sct = mss()

	# Find region with blue and create bounding box from that
	sct_img = sct.grab(bounding_box)
	img = np.array(sct_img)
	M, N, _ = img.shape

	# Image Grayscale/Processing
	im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	im = cv2.GaussianBlur(im, (5,5), 0)
	im = cv2.Canny(im, threshold1=100, threshold2=255)

	lines = cv2.HoughLines(im,1,np.pi/180,1000)

	top = 0
	bottom = 0
	if lines is not None:
		for i in range(0,2):
			rho = lines[i][0][0]
			theta = lines[i][0][1]
			a = np.cos(theta)
			b = np.sin(theta)
			y0 = b*rho
			y1 = int(y0 + 10000*(a))
			if i == 0:
				bottom = y1
			else:
				top = y1

	# New BBox that encompases the blue zone
	bounding_box = {'top': top, 'left': 0, 'width': width, 'height': bottom-top}

	sct_img = sct.grab(bounding_box)
	img = np.array(sct_img)
	img = cv2.resize(img, (0,0), fx=1.25, fy=1.25)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)[1]
	blacklist = "-c tessedit_char_blacklist=\\|"
	string = pytesseract.image_to_string(img, config=blacklist)
	string = string.replace('\r', '').replace('\n', "___").replace("Typing Test", "")
	string = string.replace("How many words per minute can you type?","").replace("___", " ").replace("  "," ").strip()
	string = string[::-1].replace("Start typing to begin"[::-1], "", 1)[::-1]
	print(string)
	pyautogui.write(string)






seconds = 3
while seconds > 0:
	print("Starts in...",seconds)
	time.sleep(1)
	seconds -= 1
main()