import cv2

class Parking:
	def __init__(self,_minx,_miny,_maxx,_maxy,_name):
		self.minx = _minx
		self.miny = _miny
		self.maxx = _maxx
		self.maxy = _maxy
		self.state = False
		self.name = _name
	
	def draw(self,img):
		if self.state == True:
			cv2.rectangle(img, (self.minx, self.miny), (self.maxx, self.maxy), (0, 0, 255), 3)
		else:
			cv2.rectangle(img, (self.minx, self.miny), (self.maxx, self.maxy), (0, 255, 0), 3)
	
	def isOcupatedBy(self,someBlob):
		if (someBlob.centerx >= self.minx and someBlob.centerx <= self.maxx) and (someBlob.centery >= self.miny and someBlob.centery <= self.maxy):
			print("BLOB " + str(someBlob.id) + " IS INSIDE PARKING " + self.name)
			self.state = True
			return True
		else:
			self.state = False
			return False