import numpy as np
import cv2
from video_source.Video import Video
import os

def captureImages():
	webcam =  Video()
	imgId = 0

	while imgId<10:
		os.system('clear')
		print('Presione ESPACIO para capturar imagen')
		print('Imagenes restantes: ' + str(10-imgId))
		
		img = webcam.getFrame()
		imgResized = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2))
		cv2.imshow('Camara', imgResized)
		key = cv2.waitKey(100)
		if key == 32:
			cv2.imshow('Captura', imgResized)
			cv2.imwrite('./camera_data/calibration-image-'+str(imgId)+'.jpg',img)
			imgId += 1

	webcam.release()
	cv2.destroyAllWindows()

	print('Proceso de captura de imagenes finalizado.')
	input('Presione una tecla para finalizar')
