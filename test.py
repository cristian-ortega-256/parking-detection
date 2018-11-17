import cv2
import numpy as np
from video_source.Video import Video
from movement_detection.MovementDetector import MovementDetector
from movement_detection.Blob import Blob
from parking_configuration.Parking import Parking
from math import sqrt
from video_source.CameraStreaming import CameraStreaming
from video_source.VideoStream import VideoStream
import json,codecs
from UserInterface import UserInterface
from helpers.JsonManager import writeToJSONFile,getHomography
import os
import requests,random
from services.api import get
from services.apiRoutes import *
from services.parkings import getParkings,putParkings

# Getting server config data

response = get(CONFIG)
configData = json.loads(response.content.decode('utf-8'))

ip = configData['ip']
port = int(configData['port'])

# Video resource

print("http://{}:{}/video".format(ip,port))

webcam = VideoStream("http://{}:{}/video".format(ip,port)).start()
#webcam =  Video("./assets/Test2.mp4")

# ---------------------------

#webcam = VideoStream(0).start()
#webcam = VideoStream(0,False).start()

# ---------------------------

blobCounter = 0

blobs = []

posibleBlobs = []

# PARKING DEFINITIONS

parkingSlots = []

userInterface = UserInterface(webcam,parkingSlots)

userInterface.start()

userInterface.parkingSlots = parkingSlots

# SET FIRST FRAME

firstFrame = userInterface.getUiFrame()

height, width, channels = firstFrame.shape

# Getting first couple of frames to initialize the move detection

movementDetector = MovementDetector(firstFrame)

homography = getHomography()

print(homography)

while True:
	# Get homography fram from source
	frame = userInterface.getUiFrame()
	# Apply movement detector to the current frame
	frameMovement = movementDetector.detectMovement(frame)
	# cv2.imshow("FrameMovementDetected",frameMovement)
	
	# TODO --> Separete blob detection in a new file

	# Current frame blobs
	currentBlobs = []
	lastFrameParkings = parkingSlots.copy()

	# Analize the movement to find contours
	(_, cnts, _) = cv2.findContours(frameMovement.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	# loop over the contours to find BLOBS
	for c in cnts:
		# if the area is too small, ignore it
		if cv2.contourArea(c) > 2000:
			# Normal BLOB
			(x, y, w, h) = cv2.boundingRect(c)
			blob = Blob(x,y,w,h,c)
			currentBlobs.append(blob)

			# # Transformed BLOB
			# points = np.array([[x,y],[x+w,y],[x,y+h],[x+w,y+h]], dtype='float32')
			# points = np.array([points])
			# transformed = cv2.perspectiveTransform(points,homography)
			# points = []
			# for point in transformed[0]:
			# 	points.append((point[0],point[1]))
			# cv2.rectangle(frame, (points[0][0],points[0][1]), (points[3][0],points[3][1]), (0,255,255), 2)
			# # blob = Blob(points[0][0],points[0][1],w,h,c)
			# # currentBlobs.append(blob)
			# print('- - - - - - - - - - - - - - - - - - - - - - - - - - -')


	# Match currentBlobs with history blobs
	if len(posibleBlobs) == 0:
		for blob in currentBlobs:
			blob.id = blobCounter
			blobCounter += 1
			posibleBlobs.append(blob)
	else:
		for cBlob in currentBlobs:
			#print(len(currentBlobs))
			distance = 99999
			matched = None
			for i in range(len(posibleBlobs)):
				blob = posibleBlobs[i]
				dist = sqrt( (cBlob.x - blob.x)**2 + (cBlob.y - blob.y)**2 )
				if dist < distance:
					distance = dist
					matched = i
			# Update blob case
			if distance < 90:
			#if distance < 30:
				blob = posibleBlobs[matched]
				cBlob.id = blob.id
				cBlob.lifeSpan = 5
				cBlob.framesAlive = blob.framesAlive + 1
				posibleBlobs[matched] = cBlob
			# Create blob case
			else:
				#cBlob.lifeSpan = 5
				if cBlob.id == None:
					cBlob.id = blobCounter
					blobCounter += 1
				posibleBlobs.append(cBlob)

	for blob in posibleBlobs:
		if(blob.lifeSpan > 0):
			blob.lifeSpan -= 1
			#blob.show(frame)


	#cv2.imshow("Frame",frame)
	#cv2.waitKey(1)
	print("----------------------------------")

userInterface.stop()
webcam.stop()
cv2.destroyAllWindows()