import numpy as np
import json,codecs

def getHomography():
    obj_text = codecs.open('./camera_data/homography.json', 'r', encoding='utf-8').read()
    b_new = json.loads(obj_text)
    return np.array(b_new)
import json
import numpy as np
import json,codecs

def writeToJSONFile(path, fileName, data):
	filePathNameWExt = './' + path + '/' + fileName + '.json'
	with open(filePathNameWExt, 'w') as fp:
	json.dump(data, fp)

def readJSONFile(path, fileName):
    filePathName = './' + path + '/' + fileName + '.json'
    with open(filePathName) as json_file:
            data = json.load(json_file)
            return data
