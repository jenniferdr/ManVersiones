import Pyro4.util
import Pyro4
import sys
from peticion import Peticion

print("# agumentos {0}.".format(len(sys.argv)))
version = ""
if(len(sys.argv) < 4 or len(sys.argv) >5):
    print("Sintaxis: client <accion> <archivo> <ipSwitch> [version-para update]")
    exit()

tipoP = sys.argv[1]
archivo = sys.argv[2]
ip= sys.argv[3]

sys.excepthook=Pyro4.util.excepthook
switch=Pyro4.Proxy('PYRO:example.switch@'+ip+':5000')
#switch.setTimeout(15)    
if(len(sys.argv) == 4):
    if(sys.argv[1]=="commit"):
      try:
         f = open(archivo)
         lectura = f.read()    
         pet1 = Peticion(tipoP,archivo,'1',lectura)
         pet1.enviarRequest(switch)
      except IOError:
         print 'No existe', archivo
			
    elif(sys.argv[1]=="checkout" or sys.argv[1]=="update"):
         pet1 = Peticion(tipoP,archivo,0,'')
         pet1.enviarRequest(switch)
	
    else:
	print("Sintaxis:client <commit|checkout|update> <archivo> [version]")
	exit()
	
elif(len(sys.argv)==5):
    if(sys.argv[1]=="update"):
         version = sys.argv[4]
         pet1 = Peticion(tipoP,archivo,version,'')
         pet1.enviarRequest(switch)
    else:
	     print("Sintaxis update: <update> <archivo> [version]")
	     exit()
	
def error(a,o):
	if (o==0):
		print ("Debe dar el path completo del archivo {0} | Debe existir").format(a)
		exit()
 
			
    
	
	

