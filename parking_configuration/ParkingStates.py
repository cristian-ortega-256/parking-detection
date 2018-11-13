import cv2
import numpy as np
import os
from helpers.JsonManager import readParkingsJSON,writeToJSONFile,writeParkingsJSON
from parking_configuration.Parking import Parking

parks = []

def mouse_action(event, x, y , flags, params):
    print(len(params))
    if event == cv2.EVENT_LBUTTONDOWN:
        for p in params:
            if p.setState((x,y), not p.state):
                break


def ParkingStates(frame):
    parks = readParkingsJSON()
    
    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", mouse_action,parks)

    print("Modifique el estado de cada estacionamiento hacienco click sobre cada uno.")
    print("Presione la tecla ESC para finalizar.")

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
    writeParkingsJSON(parks)

    cv2.destroyAllWindows()