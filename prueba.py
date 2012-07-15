from Tools import *
import Pyro4.util
import Pyro4
import socket
import sys




def main ():
	multicast('127.0.0.1','5954','hola gente','0')
	EligeCoordinador('127.0.0.1','8083','127.0.0.1','5954')

if __name__=="__main__":
    main()


