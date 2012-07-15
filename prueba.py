from Tools import *
import Pyro4.util
import Pyro4
import socket
import sys




def main ():
	multicast('127.0.0.1','5955','hola gente','0')
	EligeCoordinador('127.0.0.1','8081','127.0.0.1','5955')

if __name__=="__main__":
    main()


