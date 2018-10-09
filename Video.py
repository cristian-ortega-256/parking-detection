import cv2
import numpy as np

class Video:

	# Initialize with the integrated webcam for default
	def __init__(self,source=0):
		self.cap = cv2.VideoCapture(source)
		self.record = False

	def read(self):
		return self.cap.read()
		
	def getFrame(self):
		frame = self.cap.read()[1]
		return frame
	
	def release(self):
		self.cap.release()
