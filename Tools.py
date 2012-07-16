import Pyro4.util
import Pyro4
import socket
import sys
#import pdb
from switch import *

#(str,str,str,str) envia el mensaje al grupo simulando multicast
def multicast(ip_resolvedor,port_resolvedor,mensaje,grupo,tag = 'MULTICAST'):
	print('COSA{0}'.format(tag))
	buffsize = 2
	while buffsize <  sys.getsizeof(mensaje):
		buffsize *= buffsize
	socket_resolvedor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se Instancia un socket
	socket_resolvedor.connect((ip_resolvedor,int(port_resolvedor))) #Se conecta al resolvedor (address,port)
	socket_resolvedor.sendall(tag) #Se le envia la cadena 'MULTICAST'
	b = socket_resolvedor.recv(1024) 
	if  b != 'ACK': #Se espera un ack por parte del resolvedor
		print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
		socket_resolvedor.sendall(tag)
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
	print('COSO')


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
	
def UploadAResolvedor(ip_destino,port_destino,nombre,mensaje):


	socket_resolvedor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se Instancia un socket
	socket_resolvedor.connect((ip_destino,int(port_destino))) #Se conecta al servidor (address,port)
	socket_resolvedor.sendall('U/{0}'.format(nombre)) #Se le envia la cadena con el nombre del archivo
	buffsize = 2

	b = socket_resolvedor.recv(1024) 
	while buffsize <  sys.getsizeof(mensaje):

		buffsize *= buffsize

	print(buffsize)
	socket_resolvedor.sendall(str(buffsize)) #Se le envia la cadena con el tamano del mensaje/archivo
	print('pedir ack')

	b = socket_resolvedor.recv(1024) 
	print('2')
	if  b != 'ACK': #Se espera un ack por parte del resolvedor
		print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
		socket_resolvedor.sendall(str(buffsize))
	socket_resolvedor.sendall(mensaje) #Se envia el mensaje
	if  b != 'ACK': #Se espera un ack por parte del resolvedor
		print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
		socket_resolvedor.sendall(mensaje) 
	socket_resolvedor.close() #Se cierra el socket


def UploadAServidor(ip_destino,port_destino,nombre,mensaje):
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

	socket_resolvedor.sendall('U/{0}'.format(nombre)) #Se le envia la cadena con el nombre del archivo
	b = socket_resolvedor.recv(1024) 
	if  b != 'ACK': #Se espera un ack por parte del resolvedor
		print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
		socket_resolvedor.sendall(str(buffsize))
	while buffsize <  sys.getsizeof(mensaje):
		buffsize *= buffsize

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

def MensajesAServidor(ip_destino,port_destino,mensajes):
	socket_resolvedor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se Instancia un socket
	socket_resolvedor.connect((ip_destino,int(port_destino))) #Se conecta al servidor (address,port)
	for mensaje in mensajes:
		buffsize = 2
		while buffsize <  sys.getsizeof(mensaje):
			buffsize *= buffsize
		socket_resolvedor.sendall(str(buffsize)) #Se le envia la cadena con el tamano del mensaje/archivo
		b = socket_resolvedor.recv(1024) 
		if  b != 'ACK': #Se espera un ack por parte del resolvedor
			print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
			socket_resolvedor.sendall(str(buffsize))
		socket_resolvedor.sendall(str(mensaje)) #Se envia el mensaje
		if  b != 'ACK': #Se espera un ack por parte del resolvedor
			print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
			socket_resolvedor.sendall(str(mensaje)) 
	socket_resolvedor.close() #Se cierra el socket
	print('SI TERMINO LA FUNCION MensajeServidor')
	

def EligeCoordinador(switch_ip,switch_port,ip_resolvedor,port_resolvedor):
	switch=Pyro4.Proxy('PYRO:example.switch@{0}:{1}'.format(switch_ip,switch_port))
	switch.elegir_coordinador(ip_resolvedor,port_resolvedor)


def Info_de_servers(ip_resolvedor,port_resolvedor):
	retorno = []
#	pdb.set_trace()
	socket_resolvedor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se Instancia un socket
	socket_resolvedor.connect((ip_resolvedor,int(port_resolvedor))) #Se conecta al servidor (address,port)
	socket_resolvedor.sendall('IP-REQUEST') 
	b = socket_resolvedor.recv(1024) 
	if  b != 'ACK': #Se espera un ack por parte del resolvedor
		print('AQUI SE ESPERABA UN ACK PERO TUVIMOS UN {0}'.format(b))
		socket_resolvedor.sendall('IP-REQUEST')	
	socket_resolvedor.sendall('ACK')
	guarda = socket_resolvedor.recv(1024)
	while  guarda!= 'END':
		socket_resolvedor.sendall('ACK')
		retorno.append(guarda)
		guarda = socket_resolvedor.recv(1024)
	socket_resolvedor.sendall('ACK')
	socket_resolvedor.close() #Se cierra el socket
	return retorno	

#def EligeCoordinador2(switch,ip_resolvedor,port_resolvedor):
#	switch.elegir_coordinador(ip_resolvedor,port_resolvedor)
