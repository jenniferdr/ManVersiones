from __future__ import print_function
import Pyro4
import peticion
import sys
import socket

class Resolvedor(object):
        
    def __init__(self):
	self.localhost =  socket.gethostname()
	self.localIp = socket.gethostbyname(self.localhost)
        self.listaIp= []
        print("Si tengo listaIp {0}".format(self.listaIp))
        self.num_reg= 0

    def guardalos(self, tipoP,nombreArch,version,archi):
	 culo = tipoP
	 t=archi
	 print ('holas {0} '.format(t))
	 print("Estoy en resolvedor {0}.".format(culo))

    def agregarServidor(self,ip):
        
        num_reg= num_reg +1
        print("Se ha registrado el servidor: {0}".format(ip))
        print("{0}".format(self.listaIp))
        
        
def main():

    if(len(sys.argv)!=3):
        print("Sintaxis incorrecta: <numero_maquinas> <numero_tolerancia>")
        exit()

    numMaq= sys.argv[1]
    # Habra que replicar los archivos k+1 veces
    k= sys.argv[2]

    resolvedor=Resolvedor()
    #print("this is {0} y el ip es {1}".format(resolvedor.localhost,
#					      resolvedor.localIp))


    Pyro4.Daemon.serveSimple(
	{
	    resolvedor: "example.resolvedor"
            },
	host = '127.0.0.1',
	port = 39437,
	ns=False)

    print(" Esperando registro inicial de todos los servidores")
    while(resolvedor.num_reg< numMaq):
        a=1

    print("El registro de las maquinas se ha completado")
    
if __name__=="__main__":
    main()
