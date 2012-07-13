from __future__ import print_function
import Pyro4
import peticion
import sys

class Switch(object):
    
    def __init__(self):
	self.coordinador = ""
	self.multicast=""
	self.tipoP = ""
	self.archivo=""
	self.version=""
	
    def guardalo(self,tipoP,archivo,version):
	self.tipoP= tipoP
	self.archivo=archivo
	self.version=version

	print("Request: {0} {1} {2}".format(self.tipoP,self.archivo,self.version))

	if(self.tipoP == "commit"):
	    print("Debo hacer commit")
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

    
