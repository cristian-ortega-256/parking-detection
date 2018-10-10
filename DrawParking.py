import cv2

class DrawParking:

    def __init__(self):    
        self.point1 = ()
        self.point2 = ()
        self.drawing = False

    def mouse_drawing(self,event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.drawing is False:
                self.point1 = (x,y)
                self.drawing = True
            else:
                self.drawing = False

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing is True:
                self.point2 = (x,y)

    def drawParking(self,frame):
        cv2.rectangle(frame, self.point1, self.point2, (0,255,0))