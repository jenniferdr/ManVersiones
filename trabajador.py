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


def receiveFile(my_socket):
    for x in range(1,4):
       connection_socket,addr = my_socket.accept()  #Acepta la proxima conexion 
       buffsize = int(connection_socket.recv(1024)) #Lee el tamano de la informacion
       connection_socket.sendall('ACK')             #Envia un Ack
       data = connection_socket.recv(buffsize)      #Lee la informacion
       connection_socket.sendall('ACK')             #Envia un ack
       print(data)


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
	print ('me registre')
	while socket_resolvedor.recv(1024) != 'ACK': #Se espera otro ack por parte del resolvedor
		socket_resolvedor.sendall(sys.argv[1]+'$'+sys.argv[5]+'$'+sys.argv[2]) 
		
	socket_resolvedor.close() #Se cierra el socket
	

	# -------- SERVER UP
	my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Se instancia el socket para recibir conexiones
	my_socket.bind(('',int(sys.argv[2]))) #Se liga a todas las interfaces disponibles y al puerto especificado
	my_socket.listen(5) #Escucha por conexione en el socket
	
	#primera vez
	# if soy coordinador
	# Tengo la tabla de ips
	# genero la tabla tabla= {'': [('','')]}
	 
	 #luego 
	 
	# si es commit recorro la tabla y veo cual fue la ultima version del archivo y que servidores tienen menos carga
					# Balanceo
					# for a in tabla
					
					#	len(tabla[a][1]))
					#
	# copio la tabla imaginaria del unico grupo1 en el resolverdor
	# mando un multicast a los n servidores que le corresponde al grupo 1
	# cuando se complete el commit 
	# llenar tabla
	# Hago pickle de la tabla para poner en un archivo
	# Cada vez que llegue una peticion debo duplicar el archivo de la tabla en todos los demas 
	# mando un hecho al switch cliente
	
	# Si es Update
	# if tengo version 
			# Busco el archivo y su version 
	# else
	# recorro la tabla de archivos y agarro al primero que tenga el archivo y la version mayor, 
	# si no contesta pues busco al siguiente y marco a trabajador como muerto
	# mando el archivo al switch - cliente
	
	# si es Checkout
	# busco en la tabla el archivo el archivo con la version mayor  y se lo mando a Switch-cliente
	# si el primero no me responde , el siguiente y lo marco como muerto 
	
	
	# si no soy coordinador 
	
	# si es commit guardo el archivo
	# si es update o checkout mando el archivo
	
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
				archivo= 'hola.txt'
				version= '3'
				accion = 'commit'
#				if (accion == 'commit'):
					
				switch.avisar((sys.argv[5],sys.argv[2]),sys.argv[3],sys.argv[4])
		elif data == 'COMMIT':
			receiveFile(my_socket)
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


