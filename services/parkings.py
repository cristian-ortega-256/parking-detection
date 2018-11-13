from .apiRoutes import CONFIG,PARKINGS
from .api import get,post,put
import json
from parking_configuration.Parking import Parking

def postParkings(parkings):
	formattedParkings = []
	for parking in parkings:
		formattedParkings.append(
			{
				"tl_x": parking.minx,
				"tl_y": parking.miny,
				"br_x": parking.maxx,
				"br_y": parking.maxy,
				"isOccupied": parking.state
			}	
		)

	data = {
		"parkings": formattedParkings
	}

	return post(PARKINGS,data)

def getParkings():
	response = get(PARKINGS)
	response = json.loads(response.content)
	parkings = []
	for parking in response:
		parking_new = Parking(parking['tl_x'],parking['tl_y'],parking['br_x'],parking['br_y'],'test',parking['isOccupied'])
		parking_new.id = parking['id']
		parkings.append(parking_new)
	return parkings


def putParkings(parkings):
	formattedParkings = []
	for parking in parkings:
		new_park = {
				"id": parking.id,
				"tl_x": parking.minx,
				"tl_y": parking.miny,
				"br_x": parking.maxx,
				"br_y": parking.maxy,
				"isOccupied": parking.state
			}
			
		formattedParkings.append(new_park)

	data = {
		"parkings": formattedParkings
	}

	return put(PARKINGS,data)