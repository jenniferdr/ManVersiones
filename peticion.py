

class Peticion(object):

    

    def __init__(self, tipoP, nombreArch,version):
	self.tipoPeticion = tipoP
	self.nombreArch = nombreArch
	self.version = version
	# faltaria el archivo como tal si es commit
	
	
    def enviarRequest(self,switch):
	print("Estoy en peticion, {0} ".format(self.tipoPeticion))
	#	tipoP = self.tipoPeticion
	switch.guardalo(self.tipoPeticion,self.nombreArch,self.version)
	
    def enviarCosas(self,resolv):
	print("Estoy en peticion, {0} ".format(self.tipoPeticion))
	resolv.guardalos(self.tipoP,self.nombreArch,self.version)
	
    
