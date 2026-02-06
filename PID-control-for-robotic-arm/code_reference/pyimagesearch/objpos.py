# Importación de librerias
import numpy as np

    """
    NOTE:
    Original implementation included additional filtering
    and hardware-specific optimizations which are not fully
    recoverable from the thesis document.
    """
"""
This version corresponds to an earlier prototype of the system.
The final thesis implementation included refinements not present here.
"""

class ObjPos:
(objx.value,objy.value,a.value,b.value,c.value,
	refa.value,refb.value,refc.value)
	#Inicialización
	def __init__(self, objx, objy, a, b, c, refa, refb, refc):
		self.objx = objx
		self.objy = objy
		self.a = a
		self.b = b
		self.c = c
		self.refa = refa
		self.refb = refb
		self.refc = refc

	def update(self):
	  rad = np.pi/180
	  #Conversión de angulos al mismo punto de referencia
	  an1 = refa.value
	  pa = (a.value*np.cos(an1*rad), a.value*np.sin(an1*rad))
	  Y = objy.value - a.value
	  X = objx.value
	  B = b.value
	  C = c.value

	  aux1 = (X*X + Y*Y - B*B - C*C)/(2*B*C)
	  aux2 = 1 - aux1*aux1
	  if aux2 > 0:
		  aux3 = np.sqrt(aux2)
		  aux4 = np.arctan(aux3/aux1)
		  aux5 = aux4/rad
		  aux6 = np.arctan(Y/X)
		  aux6 = aux6/rad
		  aux7 = np.arctan((C*aux3)/(B + C*aux1))
		  aux7 = aux7/rad
		  aux8 = aux6 - aux7

		  pb = (B*np.cos(aux8*rad), B*np.sin(aux8*rad))
		  pc = (C*np.cos(aux5*rad + aux8*rad), C*np.sin(aux5*rad + aux8*rad))
		  p1 = (pa[0]+pb[0], pa[1] + pb[1])
		  p2 = (p1[0]+pc[0], p1[1] + pc[1])
		  if p1[1] < 2 or p2[1] < 4: 
			  icn.value = 1
		  elif p1[1] >= 2 or p2[1] >= 4:
			  ntlt2.value = (180 - aux8) - refb.value #+ refb.value
			  ntlt3.value = (aux5 + aux8) + (refc.value - aux8)#+ refc.value + aux8
			  icn.value = 0

	    elif aux2 <= 0:
		    icn.value = 1