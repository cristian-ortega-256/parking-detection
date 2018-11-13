# import the necessary packages
from threading import Thread
import threading
import cv2
from helpers.JsonManager import getHomography
import datetime

class VideoStream:

	def __init__(self, src=0,homographyEnabled = True):
		# initialize the video camera stream and read the first frame
		
		# from the stream
		self.stream = cv2.VideoCapture()
		self.stream.open(src)
		(self.grabbed, self.frame) = self.stream.read()

		# Set values for homography calculation
		self.homographyEnabled = homographyEnabled
		if homographyEnabled:
			self.homography =  getHomography()
			self.height, self.width, self.channels = self.frame.shape
			self.updateHomographyFrame()
 
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		self._start = datetime.datetime.now()
		Thread(target=self.update, args=()).start()
		return self
 
	def update(self):
		# keep looping infinitely until the thread is stopped
		while self.stopped == False:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
 
			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
			if self.homographyEnabled:
				self.updateHomographyFrame()
			#print('Frame updated')
 
	def updateHomographyFrame(self):
		sizeOutput = (int(self.width*1.5),int(self.height*1.5))
		self.homographyFrame = cv2.warpPerspective(self.frame, self.homography, sizeOutput)
	
	def getFrame(self):
		# return the frame most recently read
		return self.frame.copy()
	
	def getHomographyFrame(self):
		# return the frame most recently transformed
		return self.homographyFrame.copy()
 
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		self._end = datetime.datetime.now()
		print('Elapsed time')
		print((self._end - self._start).total_seconds())