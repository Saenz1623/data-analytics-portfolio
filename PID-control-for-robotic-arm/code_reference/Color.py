#Importación de librerias
import cv2
import numpy as np

#Captura de video
cap = cv2.VideoCapture(0)

#Rango de colores para segmentacion
azulBajo = np.array([71,140,100],np.uint8)
azulAlto = np.array([114,255,255],np.uint8)

#Loop infinito
while True:
    
  #Captura de video
  ret,frame = cap.read()
  #Ejecutar si se capturo video
  if ret==True:
    
    #La imagen se rota debido a que la cámara de la Raspberry Pi
    #se encuentra rotada en el robot
    frame = cv2.flip(frame, 0)
    
    #Cambio a escala HSV
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    #Generacion de la máscara y su procesamiento para minimizar 
    #ruido
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
    
    #Desplegar ventanas
    cv2.imshow('maskAzul',mask)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
      break
cap.release()
cv2.destroyAllWindows()