import cv2
import numpy as np
from video_source.Video import Video
from movement_detection.MovementDetector import MovementDetector
from movement_detection.Blob import Blob
from parking_configuration.Parking import Parking
from math import sqrt
from video_source.CameraStreaming import CameraStreaming
from video_source.VideoStream import VideoStream
from helpers.JsonManager import getHomography
import json,codecs

# Video resource
#webcam =  Video()
#webcam =  Video("./assets/ToyParking.mp4")
#webcam = CameraStreaming('http://192.168.43.1:8080/shot.jpg')
#webcam = VideoStream("http://192.168.0.19:8080/video").start()
webcam = VideoStream("http://192.168.0.20:8080/video").start()

# LOAD HOMOGRAPHY TODO --> Extract this to a json data reader
homography = getHomography()

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
parkingSlots = []

for rawParking in jParkings:
	parking_new = Parking(rawParking['point_tl'][0],rawParking['point_tl'][1],rawParking['point_br'][0],rawParking['point_br'][1],'test')
	parkingSlots.append(parking_new)

# TOP
#parkingSlots.append(Parking(650,390,850,450,'TOP'))

# BOTTOM
#parkingSlots.append(Parking(630,570,870,670,'BOTTOM'))

# LEFT
#parkingSlots.append(Parking(340,400,530,600,'LEFT'))

# RIGHT
#arkingSlots.append(Parking(1000,400,1200,600,'RIGHT'))

while True:
	# Get homography fram from source
	frame = webcam.getHomographyFrame().copy()

	# Apply movement detector to the current frame
	frameMovement = movementDetector.detectMovement(frame)
	
	#cv2.imshow("FrameMovementDetected",frameMovement)

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
	
	# PARKING SECTION
	for parking in parkingSlots:
		for blob in posibleBlobs:
			if parking.isOcupatedBy(blob):
				break
		parking.draw(frame)
	
	# Draw blobs
	for blob in posibleBlobs:
		if(blob.lifeSpan > 0):
			blob.lifeSpan -= 1
			blob.show(frame)
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame,"Blobs detected: " + str(len(blobs)),(10,40), font, 1,(0,0,0),2,cv2.LINE_AA)
	
	cv2.imshow("Frame",frame)
	key = cv2.waitKey(1)
	if key == 13:
		break
	
	# Print to determinate end of the cicle
	print("----------------------------------")
		
webcam.release()
cv2.destroyAllWindows()