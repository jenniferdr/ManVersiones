import Pyro4.util
import Pyro4
import sys
from peticion import Peticion

print("# agumentos {0}.".format(len(sys.argv)))
version = ""
if(len(sys.argv) < 3 or len(sys.argv) >4):
    print("Sintaxis: client <accion> <archivo> [version-para update]")
    exit()

elif(len(sys.argv) == 3):
    if(sys.argv[1]=="commit"):
	tipoP = sys.argv[1]
	archivo = sys.argv[2]
	# guardar los otros parametros
	print ("commit 3")
    elif(sys.argv[1]=="checkout"):
	tipoP = sys.argv[1]
	archivo = sys.argv[2]
	# guardar los otros parametros.	
	print ("checkout 3")
    elif(sys.argv[1]=="update"):
	tipoP = sys.argv[1]
	archivo = sys.argv[2]
	print ("update 3")
	# guardar los otros parametros.
    else:
	print("Sintaxis:client <commit|checkout|update> <archivo> [version]")
	exit()
	
elif(len(sys.argv)==4):
    if(sys.argv[1]=="update"):
	tipoP = sys.argv[1]
	archivo = sys.argv[2]
	version = sys.argv[3]
	print("update 4")
	# guardar los otros parametros.
    else:
	print("Sintaxis update: <update> <archivo> [version]")
	exit()
	
sys.excepthook=Pyro4.util.excepthook
    
switch=Pyro4.Proxy('PYRO:example.switch@127.0.01:8080')
pet1 = Peticion(tipoP,archivo,version)
pet1.enviarRequest(switch);

    
 

    
	
	

