import cv2
import numpy as np
import json,codecs
from video_source.VideoStream import VideoStream
from parking_configuration.Parking import Parking
from threading import Thread
import time

class UserInterface:

	def __init__(self,source):
		self.source = source
		self.parkingSlots = self.readParkings()
		self.stopped = False
		self.uiFrame = source.getFrame()

	def start(self):
		Thread(target=self.update, args=()).start()
		return self
	
	def update(self):
		while self.stopped == False:
			frame = self.source.getFrame()
			# UPDATE PARKINGS DATA
			self.parkingSlots = self.readParkings()
			# DRAW PARKING
			for parking in self.parkingSlots:
				parking.draw(frame)
			time.sleep(.01)
			self.uiFrame = frame
			# Wait for 5 seconds
			print('SHOWING INTERFACE')

	def stop(self):
		self.stopped = True

	def getUiFrame(self):
		return self.uiFrame

	def readParkings(self):
		# READ PARKINGS DATA
		json_data = codecs.open('./camera_data/parking.json', 'r', encoding='utf-8').read()
		jParkings = json.loads(json_data)['parkings']

		# PARKING DEFINITIONS
		parkingSlots = []

		for rawParking in jParkings:
			parking_new = Parking(rawParking['point_tl'][0],rawParking['point_tl'][1],rawParking['point_br'][0],rawParking['point_br'][1],'test')
			parkingSlots.append(parking_new)

		return parkingSlots