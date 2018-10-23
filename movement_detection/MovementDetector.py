import cv2
from helpers.ImageHelpers import applyGauss,toGrayScale

class MovementDetector:
	# Initialise the movement detection with 2 initial frames
	def __init__(self,firstFrame):
		self.avgFrame = self.prepareFrame(firstFrame).copy().astype("float")

	def detectMovement(self,frame):
		frameTransformed = self.prepareFrame(frame)
		cv2.accumulateWeighted(frameTransformed, self.avgFrame, 0.5)
		frameDelta = cv2.absdiff(frameTransformed, cv2.convertScaleAbs(self.avgFrame))
		thresh = cv2.threshold(frameDelta, 20, 255,cv2.THRESH_BINARY)[1]
		return cv2.dilate(thresh, None, iterations=10)

	def prepareFrame(self,rawFrame):
		blurredFrame = applyGauss(rawFrame)
		grayFrame = toGrayScale(blurredFrame)
		return grayFrame

