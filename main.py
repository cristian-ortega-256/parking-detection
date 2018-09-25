import cv2
import numpy as np
from Video import Video
from MovementDetector import MovementDetector
from Blob import Blob
from Parking import Parking
from math import sqrt

# Video resource
#webcam =  Video()
#webcam =  Video("./assets/parking_video.mp4")
webcam =  Video("./assets/test2.mp4")

# Getting first couple of frames to initialize the move detection
movementDetector = MovementDetector(webcam.getFrame())

blobCounter = 0

blobs = []

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

	print("Current blobs " + str(len(currentBlobs)))
	print("Historycal blobs " + str(len(blobs)))

	# Match currentBlobs with history blobs
	if len(blobs) == 0:
		for blob in currentBlobs:
			blob.id = blobCounter
			blobCounter += 1
			blobs.append(blob)
	else:
		for cBlob in currentBlobs:
			distance = 99999
			matched = None
			for i in range(len(blobs)):
				blob = blobs[i]
				dist = sqrt( (cBlob.x - blob.x)**2 + (cBlob.y - blob.y)**2 )
				if dist < distance:
					distance = dist
					matched = i
			# Update blob case
			if distance < 100:
				blob = blobs[matched]
				cBlob.id = blob.id
				cBlob.lifeSpan = 5
				blobs[matched] = cBlob
				print("x: " + str(cBlob.centerx) + " y: " + str(cBlob.centery) )
			# Create blob case
			else:
				cBlob.id = blobCounter
				cBlob.lifeSpan = 5
				blobCounter += 1
				blobs.append(cBlob)
	print("----------------------------------")
	
	# PARKING SECTION
	for parking in parkingSlots:
		for blob in blobs:
			if parking.isOcupatedBy(blob):
				break
		parking.draw(frame)
	
	# Draw blobs
	for blob in blobs:
		if blob.lifeSpan > 0:
			blob.lifeSpan -= 1
			blob.show(frame)
	
	# PERSPECTIVE TRANSFORMATION
	pts1 = np.float32([[390,385], [1065, 385], [300, 680], [1280, 670]])
	pts2 = np.float32([[0, 0], [1200, 0], [0, 700], [1200, 700]])
	matrix = cv2.getPerspectiveTransform(pts1, pts2)
	'''
	CIRCLES TO DETERMINATE PARKING ZONE
	# TOP LEFT
	cv2.circle(frame, (390,385), 5, (255, 0, ), -1)
	# TOP RIGHT
	cv2.circle(frame, (1065, 385), 5, (0, 255, 0), -1)
	# BOTTOM LEFT
	cv2.circle(frame, (300, 680), 5, (0, 0, 255), -1)
	# BOTTOM RIGHT
	cv2.circle(frame, (1280, 670), 5, (0, 255, 255), -1)
	'''
	
	result = cv2.warpPerspective(frame, matrix, (1200,700))
	cv2.imshow("Perspective",result)

	cv2.imshow("Frame",frame)
	key = cv2.waitKey(1)
	if key == 13:
		break
		
webcam.release()
cv2.destroyAllWindows()