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

os.system('clear')
print('Bienvenido al modulo de configuracion del Administrador de estacionamientos [ BETA ] ')
input('Presione ENTER para continuar')

# Set video resource for all config steps
webcam =  Video("./assets/ToyParking.mp4")
frame = webcam.getFrame()

# First Step - Image Capture
os.system('clear')
if len(glob.glob('./camera-data/*.jpg')) < 10:
	print('Procederemos a capturar las imagenes.')
	input('Presione ENTER para comenzar')
	captureImages()
	print('Imagenes capturadas exitosamente.')
else:
	print('Imagenes listas para calibracion.')

# Second Step - Camera Configuration
os.system('clear')
if os.path.isfile('./camera-data/calib.npz'):
	print('La camara esta calibrada')
else:
	print('Procederemos a calibrar la camara.')
	input('Presione ENTER para comenzar')
	calibrateCamera(False)
	print('Calibracion finalizada exitosamente!')
	input('Presione una tecla para continuar...')

# Third Step - Points for Homography
os.system('clear')
homographyFrame = calculateHomography(frame)

# Fourth Step - Parking Configuration
if os.path.isfile('./camera-data/parking.json'):
	print('Los estacionamientos ya están configurados.')
else:
	parkingConfigurator()

# if os.path.isfile('parkingConfig.json'):
# 	print('Configuracion de estacionamiento detectada')
# else:
# 	print('Configurar estacionamiento (MODULO PENDIENTE)')
	#ParkingConfigurator()

# Fifth Step - Start Parking System [ BETA ]
os.system('clear')
print('Ha finalizado con exito la configuracion de sus sistema de administracion de estacionamientos!')
input('Presione una tecla para finalizar...')