from __future__ import print_function
import Pyro4
import peticion
import sys
import time
from Tools import *

class Switch(object):
    
    def __init__(self):
	self.coordinador = ""
	self.multicast=""
	self.tipoP = ""
	self.archivo=""
	self.version=""
	
    def guardalo(self,tipoP,archivo,version,archi):
	self.tipoP= tipoP
	self.archivo=archivo
	self.version=version
	self.archi= archi
	resolvedor=Pyro4.Proxy('PYRO:example.resolvedor@127.0.0.1:6000')
	resolvedor.conectado(archivo)
	#sys.excepthook=Pyro4.util.excepthook

#resolvedor=Pyro4.Proxy('PYRO:example.resolvedor@127.0.0.1:39437')
#pet1 = Peticion("Estupido","arch.txt",1,"Contenido")
#pet1.enviarCosas(resolvedor)
#ip= get_ip_address('eth0')
#resolvedor.agregarServidor(ip)

	
	print("Request: {0} {1} {2} {3}".format(self.tipoP,self.archivo,self.version, self.archi))

	if(self.tipoP == "commit"):
	    print("Debo hacer commit")
	elif(self.tipoP == "checkout"):
	    print("Debo hacer checkout")
	elif(self.tipoP == "update"):
	    print("Debo hacer update")
	else:
	    print("Ni idea de que quieres: {0}".format(self.tipoP))
	    
    def elegir_coordinador(self,ip_resolvedor,puerto_resolvedor):
		multicast(ip_resolvedor,puerto_resolvedor,"ELECCION","0")
		#multicast(ip_resolvedor,puerto_resolvedor,"ELECCION","0")
		#multicast(ip_resolvedor,puerto_resolvedor,"ELECCION","0")
		#multicast(ip_resolvedor,puerto_resolvedor,"ELECCION","0")
		#time.sleep(7)
		#multicast(ip_resolvedor,puerto_resolvedor,"COORDINADOR","0")

		 
def main():
    if (len(sys.argv)!= 4):
	print ("Sintaxis incorrecta: switch <dirIP_Resolvedor> <puerto_Resolvedor> <puerto_Switch>")
	exit()


    resolvedorAddr = sys.argv[1]
    resolvedorPort = sys.argv[2]
    portLocal = sys.argv[3]
    print("port local: {0}".format(int(portLocal)))
    # cable de multicast  para todos
    grupoTrabajadores = "todos"

    #como hacer para que maneje varios request, es decir
    # varios clientes hacen un request mas o menos al mismo tiempo
    # hilo -> c/ vez que aparezca un request
    # ni idea
    switch=Switch()
    Pyro4.Daemon.serveSimple(
	{
	    switch: "example.switch"
	},
	host= '127.0.0.1',
	port=int(portLocal),
	ns=False)
    
if __name__=="__main__":
    main()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
