#Importación de librerias

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time

#Captura de video
cap = cv2.VideoCapture(0)

#Arreglos inicializados en cero para los rangos de segmentacion
azulBajo = np.array([0,0,0],np.uint8)
azulAlto = np.array([0,0,0],np.uint8)
bajo = [0,0,0]
alto = [0,0,0]


#Función de decodificación QR
def decode(im, bajo, alto) : 
    # Busqueda de códigos QR en la imagen
    decodedObjects = pyzbar.decode(im)
    # Desencriptación de la información obtenida
    for decodedObject in decodedObjects: 
        barCode = str(decodedObject.data)
        bajo[0] = int(barCode[2:5])
        bajo[1] = int(barCode[5:8])
        bajo[2] = int(barCode[8:11])
        alto[0] = int(barCode[11:14])
        alto[1] = int(barCode[14:17])
        alto[2] = int(barCode[17:20])
    
    #Declaración de arreglos 
    bajor = np.array(bajo,np.uint8)
    altor = np.array(alto,np.uint8)
    return bajor, altor

font = cv2.FONT_HERSHEY_SIMPLEX

#Loop infinito
while True:

  #Captura de video
  ret,frame = cap.read()

  #Ejecutar si se capturo video
  if ret==True:

    #La imagen se rota debido a que la cámara de la Raspberry Pi
    #se encuentra rotada en el robot
    frame = cv2.flip(frame, 0)

    #Cambio a escala de grises para decodificacion de qr
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Decodificacion de qr para rangos de colores
    azulBajo, azulAlto = decode(im, bajo, alto)
    
    #Cambios a escala HSV
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    #Generacion de la máscara y su procesamiento para minimizar ruido
    mask = cv2.inRange(frameHSV,azulBajo,azulAlto)
    mask = cv2.medianBlur(mask,7)
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    #Busqueda de contornos en la mascara
    contornos, jerarquia = cv2.findContours(mask, cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame, contornos, -1, (255,0,0), 3)
    
    #Analisis de contornos
    for c in contornos:
        
      #Calculo de area, para discriminar objetos que sean muy pequeños
      area = cv2.contourArea(c)
   
      if area > 3000:
        
        #Calculo de momentos para encontrar el centro del objeto
        M = cv2.moments(c)
        if (M["m00"]==0): M["m00"]=1
        x = int(M["m10"]/M["m00"])
        y = int(M['m01']/M['m00'])
        
        #Dibujo del centro y contorno del objeto
        cv2.circle(frame, (x,y), 7, (0,255,0), -1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, '{},{}'.format(x,y),(x+10,y), font, 0.75,
        (0,255,0),1,cv2.LINE_AA)
        nuevoContorno = cv2.convexHull(c)
        cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 3)
        
    #Desplegar ventanas e informacion de rango
    cv2.putText(frame, str(azulAlto), (0, 100), font, 1, (0,255,255),
    2, cv2.LINE_AA)
    cv2.imshow('maskAzul',mask)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
      break
cap.release()
cv2.destroyAllWindows()