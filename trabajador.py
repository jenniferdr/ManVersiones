import Pyro4.util
import Pyro4
import sys
from peticion import Peticion

sys.excepthook=Pyro4.util.excepthook
resolvedor=Pyro4.Proxy('PYRO:example.resolvedor@127.0.0.1:39437')
pet1 = Peticion("Estupido","arch.txt",1)
pet1.enviarCosas(resolvedor);
