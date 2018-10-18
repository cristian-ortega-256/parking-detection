import cv2
from DrawParking import DrawParking
from PointsManager import PointManager

def parkingConfigurator(frame):
    end = False

    all_parkings = []

    while end == False:
        pm = PointManager()
        pointsParking = pm.pointManageFromFrame(frame)
        quantity = input('Ingrese la cantidad de estacionamientos del sector indicado: ')
        dp = DrawParking(pointsParking, quantity)
        new_parking = dp.getParkings(frame)
        #print(all_parkings)
        #print(new_parking)
        all_parkings + new_parking

        #TODO --> Add Frame resources to show parkings!
        # for p in parking:
        #     cv2.line(frame, p.point_tl, p.point_tr, (255,0,0), 3)
        #     cv2.line(frame, p.point_tr, p.point_br, (0,255,0), 3)
        #     cv2.line(frame, p.point_br, p.point_bl, (0,0,255), 3)
        #     cv2.line(frame, p.point_bl, p.point_tl, (100,100,100), 3)

        key = input('Desea agregar más estacionamientos? S/N')
        #if key == "s":
        #    continue
        if key == "n":
            end = True
        
    print("Proceso de configuración de lugares de estacionamiento finalizado.")
    input("Presione ENTER para continuar.")
