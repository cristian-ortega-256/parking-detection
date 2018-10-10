import numpy
import cv2
from DrawParking import DrawParking

cap = cv2.VideoCapture(0)

dp = DrawParking()
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", dp.mouse_drawing)

while True:
    _, frame = cap.read()
    
    if dp.point1 and dp.point2:
        dp.drawParking(frame)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()