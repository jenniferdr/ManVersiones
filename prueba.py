from Tools import *
import Pyro4.util
import Pyro4
import socket
import sys




def main ():
	multicast('127.0.0.1','6161','hola gente','0')
	EligeCoordinador('127.0.0.1','5000','127.0.0.1','6161')
	tt = Info_de_servers('127.0.0.1','6161')
	for every in tt:
		print every

if __name__=="__main__":
    main()


