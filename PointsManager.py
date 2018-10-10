import numpy as np
import cv2
from Video import Video
import os

class PointManager:

    def __init__(self):
        self.points = []
        self.idPoint = 0

    def definePoints(self,event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x,y))
            self.idPoint += 1

    def pointManage(self):
        cap = cv2.VideoCapture(0)

        os.system('cls')
        cv2.namedWindow("Frame")
        cv2.setMouseCallback("Frame", self.definePoints)

        while self.idPoint < 4:
            print('Indique cuatro puntos')
            print('Puntos restantes: ' + str(4-self.idPoint))
            
            _, frame = cap.read()

            for center_position in self.points:
                cv2.circle(frame, center_position, 5, (0,0,255), -1)

            cv2.imshow("Frame", frame)

            key = cv2.waitKey(1)
            if key == 27:
                break
        
        cap.release()
        cv2.destroyAllWindows()


        #print(*points, sep = "\n")
        
        print('Proceso de configuración finalizado.')
        input('Presione una tecla para finalizar')
        return self.points
        


