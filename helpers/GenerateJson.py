import json

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

def readJSONFile(path, fileName):
        filePathName = './' + path + '/' + fileName + '.json'
        with open(filePathName) as json_file:
                data = json.load(json_file)
                return data
