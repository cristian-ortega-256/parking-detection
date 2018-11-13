import cv2
import math
import numpy as np
from helpers.PointsManager import PointManager
from helpers.JsonManager import writeToJSONFile
from helpers.ImageHelpers import drawGrid

def findBottomYPoint(points):
	second = greatest = points[0]
	for p in points:
		if p[1]>greatest[1]:
			second = greatest
			greatest = p
		elif p[1]<greatest[1] and p[1]>second[1]:
			second = p
	return greatest,second

def generateVector(p1,p2):
	return (p1[0]-p2[0],p1[1]-p2[1])

def getClosestPointPos(point,pointsToEvaluate):
	lowestDistance = 99999999999999999
	lowestPos = 0
	for x in range(len(pointsToEvaluate)):
		distance = calculateDistance(point[0],point[1],pointsToEvaluate[x][0],pointsToEvaluate[x][1])
		if distance < lowestDistance:
			lowestDistance = distance
			lowestPos = x
	return lowestPos

def orderPointsByClosestsMatches(pointsToOrder,pointsToMatchWith):
	orderedPoints = [0,1,2,3]
	for p in pointsToOrder:
		orderedPoints[getClosestPointPos(p,pointsToMatchWith)] = p
	return orderedPoints

def calculateDistance(x1,y1,x2,y2):
	dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
	return dist

def calculateRotationDiff(v1,v2):
	numerator = v1[0]*v2[0]+v1[1]*v2[1]
	magnitudeV1 = calculateVectorMagnitude(v1)
	magnitudeV2 = calculateVectorMagnitude(v2)
	denominator = magnitudeV1*magnitudeV2
	return math.degrees(math.acos(numerator/denominator))+1

def calculateVectorMagnitude(vector):
	return math.sqrt((vector[0]**2)+(vector[1]**2))

def calculateRotationPoint(point,pivot,rotationDeg):
	translated = (point[0]-pivot[0],point[1]-pivot[1])
	x = translated[0]*math.cos(rotationDeg)-translated[1]*math.sin(rotationDeg)
	y = translated[0]*math.sin(rotationDeg)+translated[1]*math.cos(rotationDeg)
	corrected = (int(x+pivot[0]),int(y+pivot[1]))
	return corrected

def applyRotationToPoints(points,pivot,degrees):
	rotatedPoints = []
	degreesAsRadian = math.radians(degrees)
	for p in points:
		if(p[0]!=pivot[0] and p[1]!=pivot[1]):
			rotatedPoints.append(calculateRotationPoint(p,pivot,degreesAsRadian))
		else:
			rotatedPoints.append(pivot)
	return rotatedPoints

def getBiggestRectangleArea(points):
	biggestArea = 0
	p1 = (0,0)
	p2 = (1,1)
	# Iterates over all the points to find the biggest area
	for p in points:
		for pt in points:
			# If not the same point, calculate the area
			if p[0] != pt[0] and p[1]!=pt[1]:
				area = calculateRectangleArea(p,pt)
				if area > biggestArea:
					biggestArea = area
					p1 = p
					p2 = pt
	return p1,p2

def calculateRectangleArea(p1,p2):
	b = p1[0]-p2[0]
	a = p1[1]-p2[1]
	return a * b

def drawPoints(points,img,color):
	for p in points:
		cv2.circle(img, p, 4, color, -1)

def asNpArray(points):
	asArray = []

	for p in points:
		asArray.append([int(p[0]),int(p[1])])
	return np.float32(asArray)

def getRectanglePoints(p1,p2):
	p3 = (0,0)
	p4 = (0,0)
	if p1[1] < p2[1]:
		p3 = (p2[0],p1[1])
		p4 = (p1[0],p2[1])
	else:
		p3 = (p1[0],p2[1])
		p4 = (p2[0],p1[1])
	return [p1,p2,p3,p4]

def calculateHomography(source):
	rawFrame = source.copy()
	frame = source
	isConfigurating = True
	while isConfigurating:
		height, width, channels = frame.shape

		# Apply GRID to the frame
		frame = drawGrid(frame,10,10)

		# Frame COPY to work with the transformations
		transformedFrame = frame

		# Get user input points
		pointsFrame = frame
		pm = PointManager()
		pts = pm.pointManageFromFrame(pointsFrame.copy())

		# Find the 2 closest to the bottom
		greatest,second = findBottomYPoint(pts)

		# Create parallel point to calculate grades between the 2 vectors
		paralelToGreatestPoint = (greatest[0]*2,greatest[1])

		# Calculates the director vectors of the given points
		vectorOriginal = generateVector(second,greatest)
		vectorParallel = generateVector(paralelToGreatestPoint,greatest)

		# Calculates the rotation difference between the to directions
		rotationDiff = calculateRotationDiff(vectorOriginal,vectorParallel)

		# Apply Rotation Correction to points
		correctedPoints = applyRotationToPoints(pts,greatest,rotationDiff)

		p1,p2 = getBiggestRectangleArea(correctedPoints)

		outPoints = getRectanglePoints(p1,p2)

		# Match rectangle points to the corrected ones position
		# NOTE: this is made to have a correspondient order between the initial 
		# input points & the final out-put points.
		orderedOutPoints = orderPointsByClosestsMatches(outPoints,correctedPoints)

		#cv2.imshow('Transformed Frame',transformedFrame)

		# Apply HOMOGRAPHY
		pts = asNpArray(pts)

		orderedOutPoints = asNpArray(orderedOutPoints)

		h, mask = cv2.findHomography(pts, orderedOutPoints, cv2.RANSAC,1.0)

		homographyFrame = cv2.warpPerspective(transformedFrame, h, (int(width*1.1),int(height*1.1)))

		cv2.destroyAllWindows()

		cv2.imshow('Homography Frame',homographyFrame)

		print('Seleccione una opcion:')
		print('	1) Reiniciar configuracion homografica')
		print('	2) Finalizar proceso ')
		key = cv2.waitKey(0)

		if key == 49:
			frame = rawFrame
		else:
			isConfigurating = False
			
		cv2.destroyWindow('Homography Frame')
		
	# Save homography in JSON file:
	data = h.tolist()
	writeToJSONFile('./camera_data', 'homography', data)
	
	print('Homografica calculada corretamente.')
	print('Presione una tecla para continuar...')
	input('')
	cv2.destroyAllWindows()

	return homographyFrame