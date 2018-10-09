import cv2
import numpy as np
import os
import glob
from ImageCapturer import captureImages
from CameraCalibrator import calibrateCamera

os.system('clear')
print('Bienvenido al modulo de configuracion del Administrador de estacionamientos [ BETA ] ')
input('Presione ENTER para continuar')

# First Step - Image Capture
if len(glob.glob('./camera-data/*.jpg')) < 10:
	print('Procederemos a capturar las imagenes.')
	input('Presione ENTER para comenzar')
	captureImages()
	print('Imagenes capturadas exitosamente.')
else:
	print('Imagenes listas para calibracion.')

# Second Step - Camera Configuration
if os.path.isfile('./camera-data/calib.npz'):
	print('La camara esta calibrada')
else:
	print('Procederemos a calibrar la camara.')
	input('Presione ENTER para comenzar')
	calibrateCamera(False)
	print('Calibracion finalizada')

# Third Step - Parking Configuration
if os.path.isfile('parkingConfig.json'):
	print('Configuracion de estacionamiento detectada')
else:
	print('Configurar estacionamiento (MODULO PENDIENTE)')
	#ParkingConfigurator()

# Fourth Step - Start Parking System [ BETA ]