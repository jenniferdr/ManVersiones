import Pyro4.util
import Pyro4
import sys
from peticion import Peticion
import socket
import fcntl
import struct
# funcion para encontrar el ip de mi maquina
# 
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

ip= get_ip_address('eth0')


sys.excepthook=Pyro4.util.excepthook
resolvedor=Pyro4.Proxy('PYRO:example.resolvedor@127.0.0.1:39437')
pet1 = Peticion("commit","hola.txt",1,"hola.txt")
pet1.enviarCosas(resolvedor)
#resolvedor.agregarServidor(ip)
