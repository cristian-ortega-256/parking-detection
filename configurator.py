import cv2
import numpy as np
import os
import glob
from video_source.Video import Video
from camera_calibration.ImageCapturer import captureImages
from camera_calibration.CameraCalibrator import calibrateCamera
from helpers.PointsManager import PointManager
from parking_configuration.DrawParking import DrawParking
from parking_configuration.ParkingConfigurator import parkingConfigurator
from parking_configuration.ParkingStates import ParkingStates
from homography_configuration.HomographyCalculator import calculateHomography
import codecs, json
from services.api import put,post
from services.parkings import postParkings
from services.apiRoutes import *
from helpers.JsonManager import readParkingsJSON
from video_source.VideoStream import VideoStream
from services.api import get
from services.apiRoutes import *
# Getting server config data

response = get(CONFIG)
configData = json.loads(response.content.decode('utf-8'))

ip = configData['ip']
port = int(configData['port'])

# Video resource
webcam = VideoStream("http://{}:{}/video".format(ip,port),False).start()
#webcam =  Video("./assets/ToyParking.mp4")
#webcam =  Video("./assets/test2.mp4")

frame = webcam.getFrame()
height, width, channels = frame.shape

configData = {
	"configurations": [
		{
			"height": height
		},
		{
			"width": width
		}
	]
}

response = put(CONFIG,configData)

#os.system('clear')
print('Bienvenido al modulo de configuracion del Administrador de estacionamientos [ BETA ] ')
input('Presione ENTER para continuar')

# First Step - Image Capture
os.system('clear')
if len(glob.glob('./camera_data/*.jpg')) < 10:
	print('Procederemos a capturar las imagenes.')
	input('Presione ENTER para comenzar')
	captureImages()
	print('Imagenes capturadas exitosamente.')
	input('Presione ENTER para continuar...')
else:
	print('Imagenes listas para calibracion.')
	input('Presione ENTER para continuar...')

# Second Step - Camera Configuration
os.system('clear')
if os.path.isfile('./camera_data/calib.npz'):
	print('La camara esta calibrada')
	input('Presione ENTER para continuar...')
else:
	print('Procederemos a calibrar la camara.')
	input('Presione ENTER para comenzar')
	calibrateCamera(False)
	print('Calibracion finalizada exitosamente!')
	input('Presione ENTER para continuar...')

# Third Step - Points for Homography
os.system('clear')
if os.path.isfile('./camera_data/homography.json'):
	print('La correccion de imagen se encuentra configurada!.')
	input('Presione ENTER para continuar...')
else:
	print('La correccion de imagen se encuentra configurada!.')
	homographyFrame = calculateHomography(frame.copy())
	print('Configuracion de imagen finalizada.')
	input('Presione ENTER para continuar...')

# Fourth Step - Parking Configuration
os.system('clear')
if os.path.isfile('./camera_data/parking.json'):
	print('Los estacionamientos ya están configurados.')
	input('Presione ENTER para continuar...')
else:
	print('Configurar estacionamiento')
	parkingConfigurator(webcam.getFrame())
	os.system('clear')
	print('Los estacionamientos configurado exitosamente!')
	input('Presione ENTER para continuar...')

# Make new connection to get an homography frame
webcam = VideoStream("http://{}:{}/video".format(ip,port)).start()

# Fifth Step - Set states of parkings
os.system('cls') # Change this line by 'clear'
opt = input('¿Desea indicar los estados de los estacionamientos? S/N')
if opt.lower() == 's':
	ParkingStates(webcam.getHomographyFrame())
else:
	print('NO')

os.system('clear')

response = postParkings(readParkingsJSON())
#print(response)


# Sixth Step - Start Parking System [ BETA ]
print('Ha finalizado con exito la configuracion de sus sistema de administracion de estacionamientos!')
input('Presione una tecla para finalizar...')