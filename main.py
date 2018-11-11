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
from helpers.JsonManager import writeToJSONFile
import os
import requests,random
from services.api import get
from services.apiRoutes import *
from services.parkings import getParkings,putParkings

# Getting server config data

response = get(CONFIG)
configData = json.loads(response.content)

ip = configData['ip']
port = int(configData['port'])

# Video resource

webcam = VideoStream("http://{}:{}/video".format(ip,port)).start()
#webcam =  Video("./assets/Test2.mp4")
#webcam = VideoStream(0).start()

# SET FIRST FRAME

firstFrame = webcam.getHomographyFrame()

height, width, channels = firstFrame.shape

# Getting first couple of frames to initialize the move detection

movementDetector = MovementDetector(firstFrame)

# ---------------------------

blobCounter = 0

blobs = []

posibleBlobs = []

# READ PARKINGS DATA

json_data = codecs.open('./camera_data/parking.json', 'r', encoding='utf-8').read()
jParkings = json.loads(json_data)['parkings']

# PARKING DEFINITIONS
parkingsResponse = getParkings()

parkingSlots = parkingsResponse

userInterface = UserInterface(webcam,parkingSlots)

userInterface.start()

userInterface.parkingSlots = parkingSlots

while True:
	# Get homography fram from source
	frame = webcam.getHomographyFrame()
	# Apply movement detector to the current frame
	frameMovement = movementDetector.detectMovement(frame)
	#cv2.imshow("FrameMovementDetected",frameMovement)

	# TODO --> Separete blob detection in a new file

	# Current frame blobs
	currentBlobs = []

	# Analize the movement to find contours
	(_, cnts, _) = cv2.findContours(frameMovement.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	# loop over the contours to find BLOBS
	for c in cnts:
		# if the area is too small, ignore it
		if cv2.contourArea(c) > 2000:
			(x, y, w, h) = cv2.boundingRect(c)
			blob = Blob(x,y,w,h,c)
			currentBlobs.append(blob)

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
	#print("----------------------------------")

	# Match Posible blobs to real blobs
	# TODO --> Check the viability of this improvement
	'''blobs = []
	for blob in posibleBlobs:
		print("Blob " + str(blob.id) + " life-span: " + str(blob.lifeSpan))
		if blob.framesAlive > 10 and blob.lifeSpan > 0:
			if blob.id == None:
				blob.id = blobCounter
				blobCounter += 1
			blob.lifeSpan -= 1
			blobs.append(blob)'''
	
	# TODO --> Separete parking state control in a new file
	
	# PARKING SECTION
	hasParkingChanged = False

	for parking in parkingSlots:
		isOccupied = False
		for blob in posibleBlobs:
			if parking.isOccupiedBy(blob):
				hasParkingChanged = True
				isOccupied = True
				break
		if(parking.specialState):
			if(isOccupied):
				parking.specialState = False
				parking.state = isOccupied
			else:
				parking.state = True
		else:
			parking.state = isOccupied
		#parking.draw(frame)

	if(hasParkingChanged):
		response = putParkings(parkingSlots)
		print(response)

		# TODO --> Make PUT to edit the updated parkings-server-state
	
	# Draw blobs
	for blob in posibleBlobs:
		if(blob.lifeSpan > 0):
			blob.lifeSpan -= 1
			blob.show(frame)
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame,"Blobs detected: " + str(len(blobs)),(10,40), font, 1,(0,0,0),2,cv2.LINE_AA)
	
	cv2.imshow("Frame",userInterface.getUiFrame())
	key = cv2.waitKey(1)
	if key == 13:
		break
	# Print to determinate end of the cicle
	print(len(posibleBlobs))
	print("----------------------------------")

userInterface.stop()
webcam.stop()
cv2.destroyAllWindows()