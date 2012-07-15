import Pyro4.util
import Pyro4
import sys
import socket
from peticion import Peticion
import fcntl
import struct
from Tools import *

# funcion para encontrar el ip de mi maquina
# 
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def main():

	if (len(sys.argv)!= 8):
		print ("Sintaxis incorrecta: trabajador <id> <puerto> <resolvedor_address> <resolvedor_puerto> <ip_mia(cableado)> <ip_switch> <puerto_switch>")
		exit()
	"""
	yo = trabajador(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
	"""
	

	soyCoordinador = False
	switch=Pyro4.Proxy('PYRO:example.switch@{0}:{1}'.format(sys.argv[6],sys.argv[7]))

	# ------ Primer Reporte ante el resolvedor
	socket_resolvedor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se Instancia un socket
	socket_resolvedor.connect((sys.argv[3],int(sys.argv[4]))) #Se conecta al resolvedor (address,port)
	socket_resolvedor.sendall('REGISTRO') #Se le envia la cadena 'REGISTRO'
	while socket_resolvedor.recv(1024) != 'ACK': #Se espera un ack por parte del resolvedor
		socket_resolvedor.sendall('REGISTRO')
	socket_resolvedor.sendall(sys.argv[1]+'$'+sys.argv[5]+'$'+sys.argv[2]) #Se envia la cadena id$ip$port de este servidor
	while socket_resolvedor.recv(1024) != 'ACK': #Se espera otro ack por parte del resolvedor
		socket_resolvedor.sendall(sys.argv[1]+'$'+sys.argv[5]+'$'+sys.argv[2]) 
	socket_resolvedor.close() #Se cierra el socket


	# -------- SERVER UP
	my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Se instancia el socket para recibir conexiones
	my_socket.bind(('',int(sys.argv[2]))) #Se liga a todas las interfaces disponibles y al puerto especificado
	my_socket.listen(5) #Escucha por conexione en el socket
	while 1:
		connection_socket,addr = my_socket.accept() #Acepta la proxima conexion 
		buffsize = int(connection_socket.recv(1024)) #Lee el tamano de la informacion
		connection_socket.sendall('ACK') #Envia un Ack
		data = connection_socket.recv(buffsize) #Lee la informacion
		connection_socket.sendall('ACK') #Envia un ack
		print('LE LLEGO UN MENSAJE AL SERVIDOR {0} QUE DICE : {1}'.format(sys.argv[1],data))
		if data == 'ELECCION':
			soyCoordinador = True
			multicast(sys.argv[3],sys.argv[4],'ID${0}'.format(sys.argv[1]),'0')
		elif 'ID$' in data:
			idd = data.split('$')[1]
			if idd != sys.argv[1] and int(idd) > int(sys.argv[1]):
				soyCoordinador = False
				print('ya no creo que sea coordinador')
		elif data == 'COORDINADOR':
			if soyCoordinador:
				switch.avisar(sys.argv[1],sys.argv[3],sys.argv[4])
		connection_socket.close()
	my_socket.close()

	print("Esta levantado el servidor {0}".format(sys.argv[1]))
   	
if __name__=="__main__":
    main()


#sys.excepthook=Pyro4.util.excepthook
#resolvedor=Pyro4.Proxy('PYRO:example.resolvedor@127.0.0.1:39437')
#pet1 = Peticion("Estupido","arch.txt",1,"Contenido")
#pet1.enviarCosas(resolvedor)
#ip= get_ip_address('eth0')
#resolvedor.agregarServidor(ip)


