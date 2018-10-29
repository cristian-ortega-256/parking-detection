import cv2
import numpy as np
from parking_configuration.Parking import Parking
from threading import Thread
import time

class UserInterface:

	def __init__(self,source,parkingSlots):
		self.source = source
		self.parkingSlots = parkingSlots
		self.stopped = False
		self.uiFrame = source.getHomographyFrame()

	def start(self):
		Thread(target=self.update, args=()).start()
		return self
	
	def update(self):
		while self.stopped == False:
			frame = self.source.getHomographyFrame()
			# DRAW PARKING
			for parking in self.parkingSlots:
				parking.draw(frame)
			time.sleep(.01)
			self.uiFrame = frame
			#print('SHOWING INTERFACE')

	def stop(self):
		self.stopped = True

	def getUiFrame(self):
		return self.uiFrame
