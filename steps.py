import cv2
import numpy as np
import os
import glob
from Video import Video
from ImageCapturer import captureImages
from CameraCalibrator import calibrateCamera
from PointsManager import PointManager
from DrawParking import DrawParking
from ParkingConfigurator import parkingConfigurator
from HomographyCalculator import calculateHomography
import codecs, json

os.system('clear')
print('Bienvenido al modulo de configuracion del Administrador de estacionamientos [ BETA ] ')
input('Presione ENTER para continuar')

# Set video resource for all config steps
#webcam =  Video("./assets/ToyParking.mp4")
webcam =  Video("./assets/test2.mp4")
frame = webcam.getFrame()

# First Step - Image Capture
os.system('clear')
if len(glob.glob('./camera-data/*.jpg')) < 10:
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
if os.path.isfile('./camera-data/calib.npz'):
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
if os.path.isfile('./camera-data/homography.json'):
	print('La correccion de imagen se encuentra configurada!.')
	input('Presione ENTER para continuar...')
else:
	print('La correccion de imagen se encuentra configurada!.')
	homographyFrame = calculateHomography(frame)
	print('Configuracion de imagen finalizada.')
	input('Presione ENTER para continuar...')

# Fourth Step - Parking Configuration
os.system('clear')
if os.path.isfile('./camera-data/parking.json'):
	print('Los estacionamientos ya están configurados.')
	input('Presione ENTER para continuar...')
else:
	print('Configurar estacionamiento')
	parkingConfigurator(webcam.getFrame())
	os.system('clear')
	print('Los estacionamientos configurado exitosamente!')
	input('Presione ENTER para continuar...')

# Fifth Step - Start Parking System [ BETA ]
os.system('clear')
print('Ha finalizado con exito la configuracion de sus sistema de administracion de estacionamientos!')
input('Presione una tecla para finalizar...')