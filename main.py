import cv2
import numpy as np
from Video import Video
from MovementDetector import MovementDetector
from Blob import Blob
from Parking import Parking
from math import sqrt

# Video resource
#webcam =  Video()
webcam =  Video("./assets/parking_video.mp4")
#webcam =  Video("./assets/test2.mp4")

firstFrame = webcam.getFrame()

height, width, channels = firstFrame.shape

# Getting first couple of frames to initialize the move detection
movementDetector = MovementDetector(firstFrame)

# ---------------------------

blobCounter = 0

blobs = []

posibleBlobs = []

# PARKING DEFINITIONS
parkingSlots = []

# TOP
parkingSlots.append(Parking(650,390,850,450,'TOP'))

# BOTTOM
parkingSlots.append(Parking(630,570,870,670,'BOTTOM'))

# LEFT
parkingSlots.append(Parking(340,400,530,600,'LEFT'))

# RIGHT
parkingSlots.append(Parking(1000,400,1200,600,'RIGHT'))

while True:
	frame = webcam.getFrame()

	frameMovement = movementDetector.detectMovement(frame)
	
	cv2.imshow("FrameMovementDetected",frameMovement)

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
			print(len(currentBlobs))
			distance = 99999
			matched = None
			for i in range(len(posibleBlobs)):
				blob = posibleBlobs[i]
				dist = sqrt( (cBlob.x - blob.x)**2 + (cBlob.y - blob.y)**2 )
				if dist < distance:
					distance = dist
					matched = i
			# Update blob case
			if distance < 100:
				blob = posibleBlobs[matched]
				cBlob.id = blob.id
				cBlob.lifeSpan = 5
				cBlob.framesAlive = blob.framesAlive + 1
				posibleBlobs[matched] = cBlob
			# Create blob case
			else:
				#cBlob.lifeSpan = 5
				posibleBlobs.append(cBlob)
	print("----------------------------------")

	# Match Posible blobs to real blobs
	blobs = []
	for blob in posibleBlobs:
		print("Blob " + str(blob.id) + " life-span: " + str(blob.lifeSpan))
		if blob.framesAlive > 10 and blob.lifeSpan > 0:
			if blob.id == None:
				blob.id = blobCounter
				blobCounter += 1
			blob.lifeSpan -= 1
			blobs.append(blob)
	
	# PARKING SECTION
	for parking in parkingSlots:
		for blob in blobs:
			if parking.isOcupatedBy(blob):
				break
		parking.draw(frame)
	
	# Draw blobs
	for blob in blobs:
		blob.show(frame)
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame,"Blobs detected: " + str(len(blobs)),(10,40), font, 1,(0,0,0),2,cv2.LINE_AA)
	
	cv2.imshow("Frame",frame)
	key = cv2.waitKey(1)
	if key == 13:
		break
		
webcam.release()
cv2.destroyAllWindows()