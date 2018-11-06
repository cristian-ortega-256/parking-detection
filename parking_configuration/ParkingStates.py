import cv2
import numpy as np
import os
from helpers.JsonManager import readJSONFile
from helpers.JsonManager import writeToJSONFile
from parking_configuration.Parking import Parking

parks = []

def mouse_action(event, x, y , flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        for p in parks:
            if p.setState((x,y), not p.state):
                break


def ParkingStates():
    cap = cv2.VideoCapture("./assets/Test2.mp4")

    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", mouse_action)

    data = readJSONFile('./camera_data', 'parking')

    for parking in data['parkings']:
        new_parking = Parking(parking['point_tl'][0],parking['point_tl'][1],parking['point_br'][0],parking['point_br'][1],parking['id'])
        parks.append(new_parking)

    print("Modifique el estado de cada estacionamiento hacienco click sobre cada uno.")
    print("Presione la tecla ESC para finalizar.")
    
    _, frame = cap.read()

    while True:

        for p in parks:
            p.draw(frame)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(100)
        if key == 27:
            break


    # Delete last json file
    os.remove("./camera_data/parking.json")

    # Save the parkings with the new states in JSON file:
    data_w = {}
    data_w['parkings'] = []
    for x in range(len(parks)):
        data_w['parkings'].append({
            'id': str(x),
            'point_tl': [parks[x].minx, parks[x].miny],
            'point_br': [parks[x].maxx, parks[x].maxy],
            'state': parks[x].state
        })
    writeToJSONFile('./camera_data', 'parking', data_w)

    cap.release()
    cv2.destroyAllWindows()