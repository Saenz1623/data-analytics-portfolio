# importacion de librerias
import cv2
import numpy as np
import pandas as pd

class ObjCenter:
	#Inicialización
	def __init__(self, haarPath):
		# load OpenCV's Haar cascade face detector
		self.detector = cv2.CascadeClassifier(haarPath)

	#Función para encontrar al objeto
	def update(self, frame, frameCenter, noface, azulBajo, azulAlto):
		
		# Código para clasificador Haar Cascade
		# convert the frame to grayscale
		#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#gray = cv2.GaussianBlur(gray,(5,5),0)
		#Rangos para el color azul por si no se desea usar los 
		#códigos QR
		#azulBajo = np.array([71,140,100],np.uint8)
		#azulAlto = np.array([114,255,255],np.uint8)
		#Conversión a HSV, generación de la máscara 
		#y su procesamiento
		frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(frameHSV,azulBajo,azulAlto)
		mask = cv2.medianBlur(mask,7)
		kernel = np.ones((5,5),np.uint8)
		mask = cv2.dilate(mask, kernel, iterations=2)
		#Hallar los contornos en la máscara
		contornos, jerarquia = cv2.findContours(mask,
		cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

		# Código para clasificador Haar Cascade
		#rects = self.detector.detectMultiScale(gray,
			#scaleFactor=1.05, minNeighbors=9, minSize=(30, 30),
			#flags=cv2.CASCADE_SCALE_IMAGE)

		# Cálculo del centro del objeto de interés,
		#despreciando areas menores a los pixeles establecidos
		for c in contornos:
			area = cv2.contourArea(c)
			if area > 1000:
				M = cv2.moments(c)
				if (M["m00"]==0): M["m00"]=1
				faceX = int(M["m10"]/M["m00"])
				faceY = int(M['m01']/M['m00'])
				noface = 1
				
				return ((faceX, faceY), c, noface)

		noface = 0
		return (frameCenter, None, noface)