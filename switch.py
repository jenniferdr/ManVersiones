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
     self.gotCoordinator = False
	
   def elegir_coordinador(self,ip_resolvedor,puerto_resolvedor):
     self.gotCoordinator = False
     multicast(ip_resolvedor,puerto_resolvedor,"ELECCION","0")
     time.sleep(7)
     multicast(ip_resolvedor,puerto_resolvedor,"COORDINADOR","0")

   def avisar(self,ipp,res_add,res_port):
     if not self.gotCoordinator:
        self.gotCoordinator = True
        self.coordinador = ipp
        print('Felicitacion a {0} por ser el nuevo coordinador'.format(ipp))
     else:
        elegir_coordinador(res_add,res_port)
		

   def guardalo(self,tipoP,archivo,version,archi):
     self.tipoP= tipoP
     self.archivo=archivo
     self.version=version
     self.archi= archi

     print("Request: {0} {1} {2} {3}".format(self.tipoP,self.archivo,self.version, self.archi))

     if(self.tipoP == "commit"):
         MensajeAServidor(self.coordinador[0],self.coordinador[1],'COMMIT')	
         MensajeAServidor(self.coordinador[0],self.coordinador[1],self.archivo)
         MensajeAServidor(self.coordinador[0],self.coordinador[1],self.archi)
         MensajeAServidor(self.coordinador[0],self.coordinador[1],self.version)
     elif(self.tipoP == "checkout"):
         print("Debo hacer update")
     elif(self.tipoP == "update"):
         print("Debo hacer update")
     else:
         print("Ni idea de que quieres: {0}".format(self.tipoP))

	    
	 
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

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
