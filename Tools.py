import socket
import sys

#(str,str,str,str) envia el mensaje al grupo simulando multicast
def multicast(ip_resolvedor,port_resolvedor,mensaje,grupo):
	print('Entrando en la funcion multicast con parametros {0} {1} {2} {3}'.format(ip_resolvedor,port_resolvedor,mensaje,grupo))
	buffsize = 2
	while buffsize <  sys.getsizeof(mensaje):
		buffsize *= buffsize
	socket_resolvedor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se Instancia un socket
	socket_resolvedor.connect((ip_resolvedor,int(port_resolvedor))) #Se conecta al resolvedor (address,port)
	socket_resolvedor.sendall('MULTICAST') #Se le envia la cadena 'MULTICAST'
	b = socket_resolvedor.recv(1024) 
	if  b != 'ACK': #Se espera un ack por parte del resolvedor
		print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
		socket_resolvedor.sendall('MULTICAST')
	socket_resolvedor.sendall(grupo) #Se el id del grupo
	b = socket_resolvedor.recv(1024) 
	if  b != 'ACK': #Se espera un ack por parte del resolvedor
		print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
		socket_resolvedor.sendall(grupo)
	socket_resolvedor.sendall(str(buffsize)) #Se le envia la cadena con el tamano del mensaje/archivo
	b = socket_resolvedor.recv(1024) 
	if  b != 'ACK': #Se espera un ack por parte del resolvedor
		print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
		socket_resolvedor.sendall(str(buffsize))
	socket_resolvedor.sendall(mensaje) #Se envia el mensaje
	b = socket_resolvedor.recv(1024) 
	if  b != 'ACK': #Se espera un ack por parte del resolvedor
		print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
		socket_resolvedor.sendall(mensaje) 
	socket_resolvedor.close() #Se cierra el socket
	print('ALELUYA SALIO DE LA FUNCION multicast BIEN')


def MensajeAServidor(ip_destino,port_destino,mensaje):
	print('Inicia la funcion MensajeAServidor con parametros {0} {1} {2}'.format(ip_destino,port_destino,mensaje))
	print(mensaje)
	buffsize = 2
	while buffsize <  sys.getsizeof(mensaje):
		buffsize *= buffsize
	socket_resolvedor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se Instancia un socket
	socket_resolvedor.connect((ip_destino,int(port_destino))) #Se conecta al servidor (address,port)
	socket_resolvedor.sendall(str(buffsize)) #Se le envia la cadena con el tamano del mensaje/archivo
	b = socket_resolvedor.recv(1024) 
	if  b != 'ACK': #Se espera un ack por parte del resolvedor
		print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
		socket_resolvedor.sendall(str(buffsize))
	socket_resolvedor.sendall(mensaje) #Se envia el mensaje
	if  b != 'ACK': #Se espera un ack por parte del resolvedor
		print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
		socket_resolvedor.sendall(mensaje) 
	socket_resolvedor.close() #Se cierra el socket
	print('SI TERMINO LA FUNCION MensajeServidor')
	
	


