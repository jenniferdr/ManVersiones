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
		try:
	
				f = open(archivo)
				lectura = f.read()    
				switch=Pyro4.Proxy('PYRO:example.switch@201.211.164.206:8080')

				pet1 = Peticion(tipoP,archivo,version,lectura)
				pet1.enviarRequest(switch)
	
		except IOError:
			print 'No existe', archivo
			
	# guardar los otros parametros
			#	print ("commit 3")
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

def error(a,o):
	if (o==0):
		print ("Debe dar el path completo del archivo {0} | Debe existir").format(a)
	
 
			
    
	
	

