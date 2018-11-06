import cv2

def toGrayScale(frame):
	return cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

# First approach to movement recognition.
# TODO -->Check if this could improve future implementations.
def diffImg(olderFrame, middleFrame, lastFrame):
	d1 = cv2.absdiff(lastFrame, middleFrame)
	d2 = cv2.absdiff(middleFrame, olderFrame)
	return cv2.bitwise_and(d1, d2)

def applyGauss(img):
	# TODO --> Check if blur more blur improves performance
	return cv2.GaussianBlur(img, (5, 5), 0)

def drawGrid(source,cols,rows):
	height, width, channels = source.shape
	
	color = (255,255,255)
	stroke = 2

	colDist = round(width / cols)
	rowDist = round(height / rows)

	for i in range(cols+1):
		cv2.line(source, (colDist*i,0), (colDist*i,height), color, stroke)
	for k in range(rows+1):
		cv2.line(source, (0,rowDist*k), (width,rowDist*k), color, stroke)

	return source