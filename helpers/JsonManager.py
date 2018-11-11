import numpy as np
import json,codecs
from parking_configuration.Parking import Parking

def getHomography():
	obj_text = codecs.open('./camera_data/homography.json', 'r', encoding='utf-8').read()
	b_new = json.loads(obj_text)
	return np.array(b_new)

def writeToJSONFile(path, fileName, data):
	filePathNameWExt = './' + path + '/' + fileName + '.json'
	with open(filePathNameWExt, 'w+') as fp:
		json.dump(data, fp)

def readJSONFile(path, fileName):
	filePathName = './' + path + '/' + fileName + '.json'
	with open(filePathName) as json_file:
		data = json.load(json_file)
		return data

def readParkingsJSON():
	parks = []
	data = readJSONFile('./camera_data', 'parking')
	for rawParking in data['parkings']:
		parking_new = Parking(rawParking['point_tl'][0],rawParking['point_tl'][1],rawParking['point_br'][0],rawParking['point_br'][1],'test',rawParking['state'])
		parks.append(parking_new)
	return parks

def writeParkingsJSON(parks):
	# Save the parkings with the new states in JSON file:
	data_w = {}
	data_w['parkings'] = []
	for x in range(len(parks)):
		id = 0
		try:
			id = parks[x].id
		except AttributeError:
			id = x
			
		data_w['parkings'].append({
				'id': str(id),
				'point_tl': [parks[x].minx, parks[x].miny],
				'point_br': [parks[x].maxx, parks[x].maxy],
				'state': parks[x].state
		})
	writeToJSONFile('./camera_data', 'parking', data_w)