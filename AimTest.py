import numpy as np
import cv2
from mss import mss
import time
import pyautogui

# Processes the image and find the locations of the circles, returns the centerpoint
def process_img(original_image):
	processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

	circles = cv2.HoughCircles(processed_img, 
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
               param2 = 35, minRadius = 40, maxRadius = 60)
  
	if circles is not None:
		circles = np.uint16(np.around(circles))
		for pt in circles[0, :]:
			a, b, r = pt[0], pt[1], pt[2]
			return a, b



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
	im = cv2.Canny(im, threshold1=180, threshold2=255)

	lines = cv2.HoughLines(im,1,np.pi/180,1000)

	top = 0
	bottom = 0
	if lines is not None:
		# for i in range(len(lines)):
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

	counter = 0
	while True:
		sct_img = sct.grab(bounding_box)
		if counter == 31:
			break;

		a, b = process_img(np.array(sct_img))
		pyautogui.click(a, b+top)
		counter += 1
		if (cv2.waitKey(1) & 0xFF) == ord('q'):
			cv2.destroyAllWindows()
			break



seconds = 3
while seconds > 0:
	print("Starts in...",seconds)
	time.sleep(1)
	seconds -= 1
main()