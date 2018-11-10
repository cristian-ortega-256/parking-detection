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
	for parking in data['parkings']:
		new_parking = Parking(parking['point_tl'][0],parking['point_tl'][1],parking['point_br'][0],parking['point_br'][1],parking['id'])
		parks.append(new_parking)
	return parks
