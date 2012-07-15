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

   # def imprimeAtt(self):
        

def main():

    if(len(sys.argv)!=3):
        print("Sintaxis incorrecta: <numero_maquinas> <numero_tolerancia>")
        exit()

    numMaq= sys.argv[1]
    # Habra que replicar los archivos k+1 veces
    k= sys.argv[2]

    resolvedor=Resolvedor()
    print("this is {0} y el ip es {1}".format(resolvedor.localhost,
					      resolvedor.localIp))

    Pyro4.Daemon.serveSimple(
	{
	    resolvedor: "example.resolvedor"
	    },
	host = '127.0.0.1',
	port = 39437,
	ns=False)
    
if __name__=="__main__":
    main()
