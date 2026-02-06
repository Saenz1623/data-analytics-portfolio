# El código requiere ser ejecutado desde la ventana de comandos cmd
#bajo el comando:
# python3 pan_tilt_tracking.py --cascade haarcascade_frontalface_default.xml
# Importación de archivos .py (c´odigod externos) al programa
from pyimagesearch.objcenter import ObjCenter
from pyimagesearch.pid import PID
from pyimagesearch.objidentify import ObjIdentify
from pyimagesearch.objpos import ObjPos

# Importación de librerias
import numpy as np
import argparse
import signal
import time
import sys
import cv2
from adafruit_servokit import ServoKit
import pyzbar.pyzbar as pyzbar

GPIO.setmode(GPIO.BCM)

#Constantes

#Nímero de canales de servomotor
nbPCAServo=16

#Valores angulares del PWM
MIN_IMP  =[500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
MIN_ANG  =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
MAX_ANG  =[180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]

#Ejecución de la tarjeta de control
pca = ServoKit(channels=16)

# funcion para configurar los PWM en los canales de la tarjeta
def init():
    for i in range(nbPCAServo):
        pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])

init()

# Rango de trabajo de los servomotores en busca de evitar golpes
#de su estructura
servoRange1 = (0, 150) #0 - 180
servoRange2 = (20, 45) #0 - 45
servoRange3 = (59, 100) #59 - 180
servoRange4 = (70, 150)

# Funcion signal para cancelar la ejecución del programa
def signal_handler(sig, frame):
	# disable the servos and gracefully exit
	print("[INFO] You pressed `ctrl + c`! Exiting...")
	sys.exit()
 
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

#Función para la identificación del objeto
def obj_center(args, objX, objY, centerX, centerY, panAngle, tiltAngle,
dis, icn, est, tlt2, tlt3):
  # Confugiración del signal
  signal.signal(signal.SIGINT, signal_handler)
  # Inicialización del reconocimiento de colores
  obj = ObjCenter(args["cascade"])

  #Inicialización de variables para configurar el rango de colores
  # Se inicia la captuda de video
  vs = cv2.VideoCapture(0)
  time.sleep(2.0)

  azulBajo = np.array([0,0,0],np.uint8)
  azulAlto = np.array([0,0,0],np.uint8)
  bajoar = [0,0,0]
  altoar = [0,0,0]

  # loop
  while True:
    # Captura de la imagen captada por la cámara la cual
    #se rota 180° debido a que la cámara se encuentra invertida
    ret, frame = vs.read()

    # Reducción de su resolución para un procesamiento más fluido
    alto=frame.shape[0]
    ancho=frame.shape[1]
    ratio=0.5
    frame = cv2.resize(frame, (int(ancho * ratio),
    int(alto * ratio)), interpolation = cv2.INTER_NEAREST)
    frame = cv2.flip(frame, 0)

    # Variable de estado, si el robot esta iniciando su ejecución,
    #estar´a a la espera de la información sobre que color se desea
    #reconocer
    if est.value == 0:
      im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      azulBajo, azulAlto = decode(im, bajoar, altoar)

    # Calculo del centro de la imagen
    (H, W) = frame.shape[:2]
    centerX.value = W // 2
    centerY.value = H // 2 + 40

    # Función para encontrar la ubicación del objeto
    objectLoc = obj.update(frame, (centerX.value, centerY.value),
    noface.value, azulBajo, azulAlto)
    ((objX.value, objY.value), rect, noface.value) = objectLoc

    # Información mostrada en pantalla
    cv2.circle(frame, (centerX.value, centerY.value),
    5, (0,255,0), -1)
    cv2.putText(frame, "Dis: " + str(dis.value)
    (10,30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(frame, "Angulo 2: " + str(panAngle.value)
    ,(10,50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(frame, "Angulo 3: " + str(tiltAngle.value)
    ,(10,70), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(frame, "Bandera: " + str(icn.value)
    ,(10,90), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(frame, "Color: " + str(azulBajo)
    ,(10,110), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)

    # Dibujo del contorno/Boundary box del objeto
    if rect is not None:
      nuevoContorno = cv2.convexHull(rect)
      cv2.drawContours(frame, [nuevoContorno],
      0, (255,0,0), 3)
      #for (x,y,w,h) in rect:
        #cv2.rectangle(frame,(x,y),(x+w,y+h),
        #(0,255,0),2)

    # Despliegue de la captura de video
    cv2.imshow("Pan-Tilt Face Tracking", frame)
    cv2.waitKey(1)

    # Entradas de teclado por el usuario
    k = cv2.waitKey(1) & 0xFF
    # Pasar a la fase de recogida, se ejecutar´a si se cumplen
    #con las condiciones
    if k == ord('q'):
      print('a')
      if icn.value == 0:
        #noface.value = 0
        est.value = 1
        tlt2.value = panAngle.value
        tlt3.value = tiltAngle.value

    # Inicialización del proceso PID tras leer QR
    elif k == ord('w'):
      print('b')
      est.value = 0

    # Reiniciar los valores de ejecución
    elif k == ord('e'):
      print('c')
      est.value = 4

    # Clean up del GPIO de la Raspberry Pi
    elif k == ord('r'):
      print('d')
      GPIO.cleanup()

#Función del controlador PID
def pid_process(output, p, i, d, objCoord, centerCoord, sn, est):
  # Configuración del signal, creación de un PID y su inicialización
  signal.signal(signal.SIGINT, signal_handler)
  p = PID(p.value, i.value, d.value)
  p.initialize()

	# loop 
	while True:
		if est.value == 0:
		# Calculo de error y actualización de datos
			error = centerCoord.value - objCoord.value
			if error != 0:
				output.value = p.update(error)
				#Algunos servomotores se encuentran
				#invertidos en sus movimientos angulares
				if sn == 1:
					output.value = output.value * -1
					output.value = output.value + 90
				output.value = output.value
		# Reinicio del PID
		elif est.value == 4:
			#p = PID(p.value, i.value, d.value)
			#p.initialize()
			est.value == 2

#Función para calcular la distancía a la cual se encuentra el objeto
def obj_identify(obj, objx, objy, a, b, c, d, tlt, tlt2, tlt3,
refa, refb, refc, refd):
	# Configuración del signal, creación de un calculador
	#y su inicialización
	signal.signal(signal.SIGINT, signal_handler)
	ob = ObjIdentify(a.value,b.value,c.value,d.value,tlt.value,
	tlt2.value,tlt3.value,refa.value,refb.value, refc.value,refd.value)
	ob.initialize()
	# loop
	while True:
		if est.value == 0:
			#Captura de datos
			ob = ObjIdentify(a.value,b.value,c.value,d.value,
			tlt.value,tlt2.value,tlt3.value,refa.value,
			refb.value, refc.value,refd.value)
			obj.value, objx.value, objy.value = ob.update()


#Función para calcular el ángulo que deberían tomar los servomotores
#para recoger el objeto
def obj_pos(objx, objy, a, b, c, refa, refb, refc, ntlt2, ntlt3, icn):
	# Configuración del signal, creación de un calculador
	#y su inicialización
	signal.signal(signal.SIGINT, signal_handler)
	pos = ObjPos(objx.value,objy.value,a.value,b.value,c.value,
	refa.value,refb.value,refc.value)
	pos.initialize()
	# loop 
	while True:
		if est.value == 0:
			#Captura de datos
			pos = ObjPos(objx.value,objy.value,a.value,b.value,
			c.value,refa.value,refb.value,refc.value)
			ntlt2.value, ntlt3.value, icn.value = pos.update()

#Función que controla los leds
def ledsest(icn, est):
	# Configuración del signal
	signal.signal(signal.SIGINT, signal_handler)
	# Configuración de puertos
	LED1 = 17
	LED2 = 27
	LED3 = 22
	GPIO.setup(LED1, GPIO.OUT)
	GPIO.setup(LED2, GPIO.OUT)
	GPIO.setup(LED3, GPIO.OUT)
	# loop
	while True:
		# Led color verde si se puede recoger el objeto,
		#rojo si no es posible
		if est.value == 0:
			if icn.value == 0:
				time.sleep(0.5)
				GPIO.output(LED1, GPIO.LOW)
				GPIO.output(LED2, GPIO.LOW)
				time.sleep(1)
				GPIO.output(LED3, GPIO.HIGH)
			if icn.value == 1:
				time.sleep(0.5)
				GPIO.output(LED2, GPIO.LOW)
				GPIO.output(LED3, GPIO.LOW)
				time.sleep(1)
				GPIO.output(LED1, GPIO.HIGH)

		# Led color amarillo si se encuentra en el proceso
		# de recogida
		if est.value == 1:
			time.sleep(0.5)
			GPIO.output(LED1, GPIO.LOW)
			GPIO.output(LED3, GPIO.LOW)
			time.sleep(1)
			GPIO.output(LED2, GPIO.HIGH)
		

#Función que controla el rango de operación de los servomotores
def in_range(val, start, end):
	return (val >= start and val <= end)

def set_servos(pan, tlt, tlt2,tlt3, noface, est, rtlt, rtlt2, rtlt3):
	# Configuración del signal
	signal.signal(signal.SIGINT, signal_handler)

	# loop 
	while True:
		if est.value == 0 or est.value == 2:
			# Variable que puede regresar al robot a
			#su posición de inicio
			if noface.value > 30:
				pan.value = 70
				tlt.value = 40
				tlt2.value = 60
				tlt3.value = 110
		
			panAngle = pan.value
			tltAngle = tlt.value
			tltAngle2 = tlt2.value
			tltAngle3 = tlt3.value

			# Si el angulo se encuentra dentro del rango,
			#los servomotores se mueven
			if in_range(panAngle, servoRange1[0], servoRange1[1]):
				pca.servo[0].angle = panAngle

			if est.value == 2:
				time.sleep(2)

			if in_range(tltAngle, servoRange2[0], servoRange2[1]):
				pca.servo[3].angle = tltAngle
				# Variable que solo se actualiza si el
				#servomotor se movio,
				#para mantener los calculos de distancia
				rtlt.value = tltAngle

			if est.value == 2:
				time.sleep(2)

			if in_range(tltAngle2, servoRange3[0], servoRange3[1]):
				pca.servo[4].angle = tltAngle2
				rtlt2.value = tltAngle2

			if est.value == 2:
				time.sleep(2)
		
			if in_range(tltAngle3, servoRange4[0], servoRange4[1]):
				pca.servo[7].angle = tltAngle3
				rtlt3.value = tltAngle3
			
			if est.value == 2:
				time.sleep(4)
				est.value = 0

		# Proceso de recogida 
		if est.value == 1:
			print('1')

			tltAngle2 = tlt.value
			tltAngle3 = tlt2.value

			#los servomotores son guiados de manera progresiva
			#para generar movimientos suaves
			
			time.sleep(1)
			delta_inicio=70
			n=20
			for i in range(1,n+1):
						#time.spleep(0.5)
						print("tltAngle3***:",
						tltAngle3)
						if ((i/n)*tltAngle3 > 
						delta_inicio):
							time.sleep(0.25)
							(pca.servo[4].angle =
							(i/n)*tltAngle3)
						print('pca.servo[4].angle =  
						' + str((i/n)*tltAngle3))


			time.sleep(2)
			delta_fin=160
			n=20
			for i in range(1,n+1):
						
						#time.spleep(0.5)
						print("tltAngle2***:",
						tltAngle2)
						if ((i/n)*tltAngle2 <
						delta_fin):
							time.sleep(0.25)
							(pca.servo[3].angle =
							(i/n)*tltAngle2)
						print('pca.servo[3].angle =
						' + str((i/n)*tltAngle2))
			
			time.sleep(2)

			pca.servo[11].angle =  120			
			
			time.sleep(2)
			
			delta=5
			angulo_servo_3=100
			while angulo_servo_3 >= 40:
						(angulo_servo_3 =}
						angulo_servo_3 - delta) 
						#print("tltAngle2***:",
						tltAngle2)
						time.sleep(0.25)
						(pca.servo[3].angle =
						angulo_servo_3)
						print('pca.servo[3].angle = '
						, angulo_servo_3 )			
			
			
			time.sleep(2)
			pca.servo[0].angle =  0
			pca.servo[7].angle =  60
			
			time.sleep(1)

			delta=5
			angulo_servo_4=130
			while angulo_servo_4 >= 70:
						(angulo_servo_4 = 
						angulo_servo_4 - delta) 
						#print("tltAngle2***:",
						tltAngle2)
						time.sleep(0.25)
						(pca.servo[4].angle =
						angulo_servo_4)
						print('pca.servo[4].angle =  ',
						angulo_servo_4 )



			time.sleep(4)
			pca.servo[11].angle =  180
			# Reinicio del sistema
			est.value = 4


# Comprobación de que se trata de la ejecución main
if __name__ == "__main__":
	# Configuración del parser junto a sus argumentos
	#(Clasificador Haar cascade si se desea utilizar)
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "--cascade", type=str, required=True,
		help="path to input Haar cascade for face detection")
	args = vars(ap.parse_args())

	# Inicialización del manager
	with Manager() as manager:

		# Valores enteros para las coordenadas del centro del frame
		centerX = manager.Value("i", 0)
		centerY = manager.Value("i", 0)

		# Valores enteros para las coordenadas del centro del objeto
		objX = manager.Value("i", 0)
		objY = manager.Value("i", 0)

		# Valores angulares de los servomotores para el controlador PID
		pan = manager.Value("i", 70)
		tlt = manager.Value("i", 40)
		tlt2 = manager.Value("i", 60)
		tlt3 = manager.Value("i", 110)

		# Valores angulares de los servomotores,
		#para los calculos geométricos
		rtlt = manager.Value("i", 40)
		rtlt2 = manager.Value("i", 60)
		rtlt3 = manager.Value("i", 110)

		# Valores PID del primer servomotor
		panP = manager.Value("f", 0.004)
		panI = manager.Value("f", 0.05) #0.09
		panD = manager.Value("f", 0.0005) #0.002

		# Valores PID del segundo servomotor
		tiltP = manager.Value("f", 0.003) #0.003
		tiltI = manager.Value("f", 0.05) #0.02
		tiltD = manager.Value("f", 0.0005) #0.0015
		
		# Valores PID del tercer servomotor
		tilt2P = manager.Value("f", 0.004) #0.03
		tilt2I = manager.Value("f", 0.05) #0.02
		tilt2D = manager.Value("f", 0.0005) #0.007
		
		# Valores PID del cuarto servomotor		
		tilt3P = manager.Value("f", 0.01)
		tilt3I = manager.Value("f", 0.02) #0.09
		tilt3D = manager.Value("f", 0.0015) #0.0025
		
		#Variable que podría controlar un regreso a su posición
		#de inicio del robot
		noface = manager.Value("i", 31)

		#Valores dimensionales de la estructura del robot
		#factor_alpha.Value("f")=1.2
		l1 = manager.Value("f", 9.52)
		l2 = manager.Value("f", 10.28)
		l3 = manager.Value("f", 12.14) 
		l4 = manager.Value("f", 15)

		#Valores para trasladar los valores de los servomotores
		#al plano de referencia
		ref1 = manager.Value("i", 90) 
		ref2 = manager.Value("i", 65) 
		ref3 = manager.Value("i", 110) 
		ref4 = manager.Value("i", 170)

		#Distancia del robot al objeto, coordenada
		#en X y en Y al cual deberán llegar los servomotores
		dis = manager.Value("f", 0.05)
		disx = manager.Value("f", 0.05) 
		disy = manager.Value("f", 0.05)

		#Bandera que controla si es posible recoger el objeto,
		#1 = No es posible, 0 = es posible
		icn = manager.Value("i", 1)

		#Valores angulares al cual deberan moverse los servomotores
		#para recoger el objeto
		ntlt = manager.Value("f", 0.05)
		ntlt2 = manager.Value("f", 0.05) 

		#Variable de estado
		est = manager.Value("i", 2)   

		# Declaración de los procesos
		processObjectCenter = Process(target=obj_center,
			args=(args, objX, objY, centerX, centerY, ntlt,
			ntlt2, dis, icn, est, tlt, tlt2))
		processPanning = Process(target=pid_process,
			args=(pan, panP, panI, panD, objX, centerX,1,
			est))
		processTilting = Process(target=pid_process,
			args=(tlt, tiltP, tiltI, tiltD, objY, centerY,1, est))
		processTilting2 = Process(target=pid_process,
			args=(tlt2, tilt2P, tilt2I, tilt2D, objY, centerY,0,
			est))
		processTilting3 = Process(target=pid_process,
			args=(tlt3, tilt3P, tilt3I, tilt3D, objY, centerY,
			1, est))
		processSetServos = Process(target=set_servos, args=(pan,
		tlt, tlt2,tlt3, noface, est, rtlt, rtlt2, rtlt3))
		processIdentify = Process(target=obj_identify, args=(dis,
		disx, disy, l1, l2, l3, l4, rtlt, rtlt2, rtlt3, ref1,
		ref2, ref3, ref4))
		processPos = Process(target=obj_pos, args=(disx, disy, l1,
		l2, l3, ref1, ref2, ref3, ntlt, ntlt2,icn))
		processLeds = Process(target=ledsest, args=(icn, est))

		# Inicialización de procesos
		processObjectCenter.start()
		processPanning.start()
		processTilting.start()
		processTilting2.start()
		processTilting3.start()
		processSetServos.start()
		processIdentify.start()
		processPos.start()
		processLeds.start()

		# Unión
		processObjectCenter.join()
		processPanning.join()
		processTilting.join()
		processTilting2.join()
		#processTilting3.join()
		processSetServos.join()
		processIdentify.join()
		processPos.join()
		processLeds.join()