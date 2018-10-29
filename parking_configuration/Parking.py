import cv2

class Parking:
	def __init__(self,_minx,_miny,_maxx,_maxy,_name,state):
		self.minx = _minx
		self.miny = _miny
		self.maxx = _maxx
		self.maxy = _maxy
		self.state = state
		self.specialState = state
		self.name = _name
	
	def draw(self,img):
		if self.state == True:
			cv2.rectangle(img, (self.minx, self.miny), (self.maxx, self.maxy), (0, 0, 255), 3)
		else:
			cv2.rectangle(img, (self.minx, self.miny), (self.maxx, self.maxy), (0, 255, 0), 3)
	
	def isOccupiedBy(self,someBlob):
		if (someBlob.centerx >= self.minx and someBlob.centerx <= self.maxx) and (someBlob.centery >= self.miny and someBlob.centery <= self.maxy):
			print("BLOB " + str(someBlob.id) + " IS INSIDE PARKING " + self.name)
			return True
		else:
			return False

	def setState(self, point, state):
		if ((point[0] >= self.minx and point[0] <= self.maxx) and (point[1] >= self.miny and point[1] <= self.maxy)) and state:
			self.state = state
			return True
		elif ((point[0] >= self.minx and point[0] <= self.maxx) and (point[1] >= self.miny and point[1] <= self.maxy)) and not state:
			self.state = state
			return True
		else:
			return False

	def __str__(self):
		return "Top: (%s, %s), Bottom: (%s, %s), State: %s" % (self.minx, self.miny, self.maxx, self.maxy, self.state)