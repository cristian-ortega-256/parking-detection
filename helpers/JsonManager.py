import numpy as np
import json,codecs

def writeToJSONFile(path, fileName, data):
	filePathNameWExt = './' + path + '/' + fileName + '.json'
	with open(filePathNameWExt, 'w') as fp:
		json.dump(data, fp)
		
def getHomography():
	obj_text = codecs.open('./camera_data/homography.json', 'r', encoding='utf-8').read()
	b_new = json.loads(obj_text)
	return np.array(b_new)