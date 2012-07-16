from __future__ import print_function
import Pyro4
import peticion
import sys
import socket
import atexit
import threading
import SocketServer
from Tools import *



#RESOLVEDOR CON SOCKETS MULTIHILOS

#Handler del servidor
class requestHandler(SocketServer.BaseRequestHandler):

   #def __init__(self, reques, client_address, server)

   def handle(self):
		
     data = self.request.recv(1024)#Lee la informacion sel socket a la variable 'data'
     if data == 'REGISTRO':		
        #Caso de registro de nuevo servidor
        self.request.sendall('ACK')#Envia ack
        data = self.request.recv(1024).split('$')#lee datos del socket
        self.request.sendall('ACK')#envia ack
        self.server.servers[data[0]] = (data[1],data[2])#incluye datos del servidor

        if data[0] not in self.server.groups['0']:
           #Evita duplicados en el diccionario de servidores
           self.server.groups['0'].append(data[0])
           #print("Se registro correctamente el servidor {0}
           #con los datos {1}".format(data[0],self.server.servers[data[0]]))
		   #print(self.server.groups['0'])
     elif data == 'MULTICAST':
        #Se envia un multicast
        #print('LLEGO UN MULTICAST AL RESOLVEDOR')
        self.request.sendall('ACK')#Envia ack
        grupo = self.request.recv(1024)#obtiene el grupo al que esta dirigido
        #print('LLego para el grupo {0}'.format(grupo))
        self.request.sendall('ACK')#manda ack
        buffsize = self.request.recv(1024)#obtiene el tamano del mensaje
        #print('LLego con un mensaje de buffsize {0}'.format(buffsize))
        self.request.sendall('ACK')#manda ack
        mensaje = self.request.recv(int(buffsize))#lee mensaje de socket
        #print('LLego con el mensaje {0}'.format(mensaje))
        self.request.sendall('ACK')#manda ack
        #manda los mensajes
        for server in self.server.groups[grupo]:
            info = self.server.servers[server]
            print(info)
            MensajeAServidor(info[0],info[1],mensaje)
     elif data == 'IP-REQUEST':
        print('CHEC')
        self.request.sendall('ACK')#Recibe Ack
        self.request.recv(1024)#Recibe Ack
        for id in self.server.servers:
            self.request.sendall(self.server.servers[id][0])
            self.request.recv(1024)#Recibe Ack
            print (self.server.servers[id][1])
            self.request.sendall(self.server.servers[id][1])
            self.request.recv(1024)#Recibe Ack
            self.request.sendall('END')
            self.request.recv(1024)#Recibe Ack

     else:
         print('')

#Implementacion de servidor multihilo
class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	def __init__(self, server_address, RequestHandlerClass):
		SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
		self.servers = {}
		self.groups = {'0':[]}
		self.sockets = []
		

def close_sockets(server):
	server.shutdown


#VERSION RESOLVEDOR PYRO
	
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
#        print("{0}".format(self.listaIp))
        
        
def main():

    if(len(sys.argv)!=4):
        print("Sintaxis incorrecta: <numero_maquinas> <numero_tolerancia> <puerto>")
        exit()

        
    #-------------version Pyro
    #numMaq= sys.argv[1]
    # Habra que replicar los archivos k+1 veces
    #k= sys.argv[2]

    #resolvedor=Resolvedor()
    #print("this is {0} y el ip es {1}".format(resolvedor.localhost,
#					      resolvedor.localIp))


    
    #Pyro4.Daemon.serveSimple(
	#{
	 #   resolvedor: "example.resolvedor"
      #      },
	#host = '127.0.0.1',
	#port = 39437,
	#ns=False)

    #print(" Esperando registro inicial de todos los servidores")
    #while(resolvedor.num_reg< numMaq):
     #   a=1

    #print("El registro de las maquinas se ha completado")
        
    #----------Version Sockets
    
    serv = Server(('',int(sys.argv[3])),requestHandler)
    s_thread = threading.Thread(target=serv.serve_forever)
    s_thread.demon = True
    s_thread.start()
    #Se instancia el socket para recibir conexiones
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    atexit.register(close_sockets,serv)
    while 1:
    	a = 1
    atexit.register(close_sockets,serv)
    serv.shutdown()
    
    
if __name__=="__main__":
    main()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
