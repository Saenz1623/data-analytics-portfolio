# Importación de librerias
import numpy as np

class ObjIdentify:

	#Inicialización
	def __init__(self, a,b,c,d,tlt,tlt2,tlt3,refa,refb,refc,refd):
		self.a = a
		self.b = b
		self.c = c
		self.d = d
		self.tlt = tlt
		self.tlt2 = tlt2
		self.tlt3 = tlt3
		self.refa = refa
		self.refb = refb
		self.refc = refc
		self.refd = refd

	def initialize(self):
		self.obj = 0
		self.objx = 0
		self.objy = 0

	#Cálculo geométrico
	def update(self):
		rad = np.pi/180
		#Conversión de angulos al mismo punto de referencia
		an1 = self.refa
		an2 = (180- self.tlt) - self.refb
		an3 = self.tlt2 - self.refc + an2
		an4 = (180 - self.tlt3) + self.refd + an3

		#Generación de vectores
		pa = (self.a*np.cos(an1*rad), self.a*np.sin(an1*rad))
		pb = (self.b*np.cos(an2*rad), self.b*np.sin(an2*rad))
		pc = (self.c*np.cos(an3*rad), self.c*np.sin(an3*rad))
		pd = (self.d*np.cos(an4*rad), self.d*np.sin(an4*rad))

		# Calculo de puntos
		A = pa
		B = (A[0]+pb[0],A[1]+pb[1]) 
		C = (B[0]+pc[0],B[1]+pc[1]) 
		D = (C[0]+pd[0],C[1]+pd[1])

	
		# Calculo de pendiente
		m = ((D[1]-C[1])/(D[0]-C[0]))

		# Calculo de la recta si la pendiente no es igual a cero
		if m != 0:
			#Cálculo de los puntos de interés y return
			self.obj = C[0]-C[1]/m
			J = (self.obj,0)
			K = (J[0]-pd[0],J[1]-pd[1])
			self.objx = K[0]
			self.objy = K[1]
		return (self.obj,self.objx,self.objy)