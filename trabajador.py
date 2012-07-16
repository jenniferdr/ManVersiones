import Pyro4.util
import Pyro4
import sys
import socket
from peticion import Peticion
import fcntl
import struct
from Tools import *
import pickle

# funcion para encontrar el ip de mi maquina
# 
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def receiveData(my_socket):
       connection_socket,addr = my_socket.accept()  #Acepta la proxima conexion 
       buffsize = int(connection_socket.recv(1024)) #Lee el tamano de la informacion
       connection_socket.sendall('ACK')             #Envia un Ack
       data = connection_socket.recv(buffsize)      #Lee la informacion
       connection_socket.sendall('ACK')             #Envia un ack
       return(data)


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
	lista = Info_de_servers(sys.argv[3],sys.argv[4])
	table = {}
	####
	##Cambiar!!!!
	k=4
	##
	
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
				switch.avisar((sys.argv[5],sys.argv[2]),sys.argv[3],sys.argv[4])
		elif data == 'COMMIT':
			nombre = receiveData(my_socket)
			data = receiveData(my_socket)
			version = receiveData(my_socket)
			#my_file = open('pruebas/{0}'.format(nombre),'wb')
			#my_file.write(data)
			#my_file.close()

			versionMayor=0
			menores=[]
			for i in lista:
				table[i]=[]
			for ip in table.keys():
				
				if len(menores)<k:
					menores.append(ip)
				else:
					for ipstent in menores:
						if len(table[ip])< len(table[iptent]):
							menores.remove(iptent)
							menores.append(ip)
							break
					for tupla in tabla[ip]:
						if tupla[0]== nombre:
							if tupla[1]> versionMayor:
								versionMayor= tupla[1]
			menores = ['127.0.0.1']
			pickle.dump(menores , open("listaIp", "wb"))
			archivo = open('listaIp') 
            		UploadAResolvedor(sys.argv[3],sys.argv[4],'Table-----v/0',archivo.read())
			# enviar menores
			# enviar archivo multicast data nombre archivo y version +1
			# recibir el AKC del resolverdor si todo salio bien 
			#for ip in menores:
			#	table[ip].append((nombre, versionMayor+1))
			print('COSSSSSO')		
			print(data)	
			#pickle.dump( table, open( "tablaGenral", "wb",2 ) )
			multicast(sys.argv[3],sys.argv[4],data,'0','MU/{0}/{1}'.format(nombre,'2'))

			### ENVIAR EL ARCHIVO A TODOS
			#TablaEnvio = pickle.load( open( "tablaGenral", "rb",2 ) )
		elif 'U/' in data:
			nombre = '{0}.{1}'.format(data.split('/')[1],sys.argv[1])
			version = data.split('/')[2]
			if version == None:
				Version = '0'	
			buffsize = int(connection_socket.recv(1024)) #Lee el tamano de la informacion
			connection_socket.sendall('ACK') #Envia un Ack
			data = connection_socket.recv(buffsize) #Lee la informacion
			connection_socket.sendall('ACK') #Envia un acki
			my_file = open('pruebas/{0}'.format(nombre),'wb')
			my_file.write(data)
			my_file.close()
		elif data == 'UPDATE' or data=='CHECKOUT':
			if version>0:
				for ip in tabla.keys():
					for tupla in tabla[ip]:
						if (tupla[0]== nombre and tupla[1]==version):
							print'enviar'
							# enviar al grupo => "ip" nombre + version			
			else:
			    for ip in table.keys():
					for tupla in tabla[ip]:
						if tupla[0]== nombre:
							if tupla[1]> versionMayor:
								versionMayor= tupla[1]
								grupo=ip
				# enviar grupo 
				# enviar al grupo "ip" nombre + version		
	
		 # si es Checkout
		 # busco en la tabla el archivo el archivo con la version mayor  y se lo mando a Switch-cliente
		 # si el primero no me responde , el siguiente y lo marco como muerto 

		# si no soy coordinador 
	
		# si es commit guardo el archivo
		# si es update o checkout mando el archivo
			

		connection_socket.close()
	my_socket.close()



if __name__=="__main__":
   main()





#sys.excepthook=Pyro4.util.excepthook
#resolvedor=Pyro4.Proxy('PYRO:example.resolvedor@127.0.0.1:39437')
#pet1 = Peticion("Estupido","arch.txt",1,"Contenido")
#pet1.enviarCosas(resolvedor)
#ip= get_ip_address('eth0')
#resolvedor.agregarServidor(ip)


