import cv2
from parking_configuration.DrawParking import DrawParking
from helpers.PointsManager import PointManager
from helpers.JsonManager import writeToJSONFile
import numpy as np
import json,codecs

def parkingConfigurator(frame):
    end = False

    # TODO --> Extract this to a json data reader
    obj_text = codecs.open('./camera_data/homography.json', 'r', encoding='utf-8').read()
    b_new = json.loads(obj_text)
    homography = np.array(b_new)

    height, width, channels = frame.shape

    frame = cv2.warpPerspective(frame, homography, (width,height))

    all_parkings = []

    while end == False:
        pm = PointManager()
        pointsParking = pm.pointManageFromFrame(frame)
        quantity = input('Ingrese la cantidad de estacionamientos del sector indicado: ')
        dp = DrawParking(pointsParking, quantity)
        new_parking = dp.getParkings(frame)
        #print(all_parkings)
        #print(new_parking)
        all_parkings = all_parkings + new_parking

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

    # Save the parkings in JSON file:
    data = {}
    data['parkings'] = []
    for x in range(len(all_parkings)):
        data['parkings'].append({
            'id': str(x),
            'point_tl': all_parkings[x].point_tl,
            'point_br': all_parkings[x].point_br,
            'state': True
        })
    writeToJSONFile('./camera_data', 'parking', data)
