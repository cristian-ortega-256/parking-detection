import cv2
import math
import os
from parking_configuration.ParkingSlot import ParkingSlot

class DrawParking:

    def __init__(self, _points, _quantity):    
        self.point_tl = _points[0]
        self.point_tr = _points[1]
        self.point_bl = _points[2]
        self.point_br = _points[3]
        self.quantity = int(_quantity)


    def getParkings(self,frame):
        while True:
            #cv2.line(frame, self.point_tl, self.point_tr, (0,0,255), 3)
            #cv2.line(frame, self.point_tr, self.point_br, (0,0,255), 3)
            #cv2.line(frame, self.point_br, self.point_bl, (0,0,255), 3)
            #cv2.line(frame, self.point_bl, self.point_tl, (0,0,255), 3)

            diff_width = math.hypot(self.point_tr[0] - self.point_tl[0], self.point_tr[1] - self.point_tl[1])
            diff_height = math.hypot(self.point_bl[0] - self.point_tl[0], self.point_bl[1] - self.point_tl[1])
            parkings_quantity_w = int(diff_width / self.quantity)
            parkings_quantity_h = int(diff_height / self.quantity)

            parking = []

            for x in range(1, self.quantity):
                if diff_width > diff_height:
                    point1 = (self.point_tl[0] + (parkings_quantity_w * x), self.point_tl[1])
                    point2 = (self.point_bl[0] + (parkings_quantity_w * x), self.point_bl[1])
                    #cv2.line(frame, point1, point2, (0,255,255), 2)

                    if x == 1:
                        # Save the fist parking
                        parkingSlot = ParkingSlot(self.point_tl, point1, self.point_bl, point2, x)
                        parking.append(parkingSlot)
                        print(str(parkingSlot))

                        # Save the last parking
                        point1 = (self.point_tl[0] + (parkings_quantity_w * (self.quantity - 1)), self.point_tl[1])
                        point2 = (self.point_bl[0] + (parkings_quantity_w * (self.quantity - 1)), self.point_bl[1])
                        last_point_tr = (point1[0] + parkings_quantity_w, self.point_tl[1])
                        last_point_br = (point2[0] + parkings_quantity_w, self.point_bl[1])
                        parkingSlot = ParkingSlot(point1, last_point_tr, point2, last_point_br, self.quantity)
                        parking.append(parkingSlot)
                        print(str(parkingSlot))

                    else:
                        previous_point1 = (self.point_tl[0] + (parkings_quantity_w * (x-1)), self.point_tl[1])
                        previous_point2 = (self.point_bl[0] + (parkings_quantity_w * (x-1)), self.point_bl[1])
                        parkingSlot = ParkingSlot(previous_point1, point1, previous_point2, point2, x)
                        parking.append(parkingSlot)
                        #print(str(parkingSlot))

                else:
                    point1 = (self.point_tl[0], self.point_tl[1] + (parkings_quantity_h * x))
                    point2 = (self.point_tr[0], self.point_tr[1] + (parkings_quantity_h * x))
                    #cv2.line(frame, point1, point2, (0,255,255), 2)

                    if x == 1:
                        # Save the first parking
                        parkingSlot = ParkingSlot(self.point_tl, self.point_tr, point1, point2, x)
                        parking.append(parkingSlot)
                        #print(str(parkingSlot))

                        # Save the last parking
                        point1 = (self.point_tl[0], self.point_tl[1] + (parkings_quantity_h * (self.quantity - 1)))
                        point2 = (self.point_tr[0], self.point_tr[1] + (parkings_quantity_h * (self.quantity - 1)))
                        last_point_bl = (point1[0], point2[1] + parkings_quantity_h)
                        last_point_br = (point2[0], point2[1] + parkings_quantity_h)
                        parkingSlot = ParkingSlot(point1, point2, last_point_bl, last_point_br, self.quantity)
                        parking.append(parkingSlot)
                        #print(str(parkingSlot))

                    else:
                        previous_point1 = (self.point_tl[0], self.point_tl[1] + (parkings_quantity_h * (x - 1)))
                        previous_point2 = (self.point_tr[0], self.point_tr[1] + (parkings_quantity_h * (x - 1)))
                        parkingSlot = ParkingSlot(previous_point1, previous_point2, point1, point2, x)
                        parking.append(parkingSlot)
                        #print(str(parkingSlot))

            
            for p in parking:
                cv2.line(frame, p.point_tl, p.point_tr, (255,0,0), 3)
                cv2.line(frame, p.point_tr, p.point_br, (0,255,0), 3)
                cv2.line(frame, p.point_br, p.point_bl, (0,0,255), 3)
                cv2.line(frame, p.point_bl, p.point_tl, (100,100,100), 3)


            cv2.imshow("Frame", frame)

            key = cv2.waitKey(50)
            if key == 27:
                break

        cv2.destroyAllWindows()
        return parking