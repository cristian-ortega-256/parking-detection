import cv2

class Blob:

	id = None
	
	def __init__(self,_x,_y,_height,_width,_contours):
		self.x = _x
		self.y = _y
		self.height = _height
		self.width = _width
		self.contours = _contours
	
	def show(self,img):
		cv2.rectangle(img, (self.x, self.y), (self.x + self.height, self.y + self.width), (0, 255, 0), 2)
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(img,str(self.id),(self.x+(self.width//2),self.y+(self.height//2)), font, 1,(0,255,0),2,cv2.LINE_AA)