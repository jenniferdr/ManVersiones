from __future__ import print_function
import Pyro4
import peticion
import sys
import socket

class Resolvedor(object):
        
    def __init__(self):
	self.localhost =  socket.gethostname()
	self.localIp = socket.gethostbyname(self.localhost)

    def guardalos(self, tipoP,nombreArch,version):
	 culo = tipoP
	 print("Estoy en resolvedor {0}.".format(culo))

def main():
    print("Esto es una prueba")
    resolvedor=Resolvedor()
    print("this is {0} y el ip es {1}".format(resolvedor.localhost,
					      resolvedor.localIp))

    resolvedor = Resolvedor()
    Pyro4.Daemon.serveSimple(
	{
	    resolvedor: "example.resolvedor"
	    },
	host = '127.0.0.1',
	port = 39437,
	ns=False)
    
if __name__=="__main__":
    main()
