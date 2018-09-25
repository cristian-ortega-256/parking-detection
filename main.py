import cv2
import numpy as np
from Video import Video
from MovementDetector import MovementDetector
from Blob import Blob
from math import sqrt

# Video resource
#webcam =  Video()
#webcam =  Video("./assets/parking_video.mp4")
webcam =  Video("./assets/test.mp4")

# Getting first couple of frames to initialize the move detection
movementDetector = MovementDetector(webcam.getFrame())

blobCounter = 0

blobs = []

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
		if cv2.contourArea(c) > 3000:
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
			if distance < 100:
				blob = blobs[matched]
				cBlob.id = blob.id
				blobs[matched] = cBlob
			else:
				cBlob.id = blobCounter
				blobCounter += 1
				blobs.append(cBlob)
	print("----------------------------------")

	# Draw blobs
	for blob in blobs:
		blob.show(frame)
		
	cv2.imshow("Frame",frame)
	key = cv2.waitKey(1)
	if key == 13:
		break

webcam.release()
cv2.destroyAllWindows()