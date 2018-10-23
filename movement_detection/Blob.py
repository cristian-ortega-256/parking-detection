import cv2

class Blob:

	id = None
	lifeSpan = 5
	framesAlive = 0
	
	def __init__(self,_x,_y,_height,_width,_contours):
		self.x = _x
		self.y = _y
		self.height = _height
		self.width = _width
		self.contours = _contours
		self.centerx = _x + _height // 2
		self.centery = _y + _width // 2
	
	def show(self,img):
		cv2.rectangle(img, (self.x, self.y), (self.x + self.height, self.y + self.width), (255, 0, 0), 2)
		cv2.circle(img, (self.centerx, self.centery), 5, (0, 255, 255), -1)
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(img,str(self.id),(self.centerx-15,self.centery-15), font, 1,(255,0,0),2,cv2.LINE_AA)