# Using Android IP Webcam video .jpg stream (tested) in Python2 OpenCV3

import urllib
import cv2
import numpy as np
import time
import logging

class CameraStreaming:

	def __init__(self,url):
		self.url = url

	def getFrame(self):
		try:
			# Use urllib to get the image from the IP camera
			imgResp = urllib.urlopen(self.url)
			
			# Numpy to convert into a array
			imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
			
			# Finally decode the array to OpenCV usable format
			return cv2.imdecode(imgNp,-1)
		except Exception as e:
			logging.exception(e)