from Tools import *
import Pyro4.util
import Pyro4
import socket
import sys




def main ():
	multicast('127.0.0.1','2000','hola gente','0')
	EligeCoordinador('127.0.0.1','2000','127.0.0.1','2500')

if __name__=="__main__":
    main()


