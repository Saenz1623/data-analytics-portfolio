# Importación de librerias
import time

class PID:
	#Inicialización
	def __init__(self, kP=1, kI=0, kD=0):
		self.kP = kP
		self.kI = kI
		self.kD = kD

	def initialize(self):
		# Inicialización del tiempo actual y pasado
		self.currTime = time.time()
		self.prevTime = self.currTime

		# Inicialización del error previo
		self.prevError = 0

		# Inicialización de las variables
		self.cP = 0
		self.cI = 0
		self.cD = 0

	#Función para la ejecución del proceso PID
	def update(self, error, sleep=0.2):
		time.sleep(sleep)

		# Calculo de la diferencia de tiempo
		self.currTime = time.time()
		deltaTime = self.currTime - self.prevTime

		# Calculo de la diferencia de errores
		deltaError = error - self.prevError

		# Calculo del termino proporcional
		self.cP = error

		# Calculo del termino integral
		self.cI += error * deltaTime

		# Calculo del termino derivativo evitando dividir entre cero
		self.cD = (deltaError / deltaTime) if deltaTime > 0 else 0

		# Guardar el tiempo y error previo para la siguiente 
		#actualización
		self.prevTime = self.currTime
		self.prevError = error

		# Suma de los terminos para return
		return sum([
			self.kP * self.cP,
			self.kI * self.cI,
			self.kD * self.cD])