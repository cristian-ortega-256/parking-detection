import requests,json

url = 'http://127.0.0.1:8000/api'

headers = {"Content-Type": "application/json"}

def get(resource):
	return requests.get("{}{}".format(url,resource), headers=headers)

def post(resource,data):
	return requests.post("{}{}".format(url,resource),data=json.dumps(data), headers=headers)

def put(resource,data):
	return requests.put("{}{}".format(url,resource),data=json.dumps(data), headers=headers)
