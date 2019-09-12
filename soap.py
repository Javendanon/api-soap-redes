
import logging
logging.basicConfig(level=logging.DEBUG)
from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode
from spyne import Iterable
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from spyne.model.primitive import String


class digitoVerificadorService(ServiceBase):

    @rpc(Unicode,Integer, _returns = Iterable(Unicode))
    def digitoVerificador(ctx,rut,times):
        # yield 'Hola senor %s' % rut
        completeRut = rut.split('-')
        rutUsable = completeRut[0]
        if (len(rutUsable)<7):
            error = 'Error: El rut ingresado '+ rut + ' no es valido'
            yield error
        else:
            suma = 0
            k=2
            rutInvertido = rutUsable[::-1]
            for i in range(len(rutUsable)):
                if (i<6):
                    suma = suma + int(rutInvertido[i])*k
                    k+=1
                elif (i==6):
                    k=2
                    suma += int(rutInvertido[i])*k
                else:
                    k+=1
                    suma += int(rutInvertido[i])*k
            dv = 11-(suma%11)
            if (dv== int(completeRut[1])):
                if (dv==10):
                    msg = 'El rut ingresado '+ rut + ' es valido y tiene como digito verificador K'
                    yield msg
                elif (dv ==11):
                    msg = 'El rut ingresado '+ rut +' es valido y tiene como digito veriicador 0'
                    yield msg
                else:
                    msg = 'El rut ingresado ' + rut + 'es valido y tiene como digito verificador ' + completeRut[1]
                    yield msg
            else:
                msg = 'El rut ingresado ' + rut + ' es invalido o el formato esta errado'

# class nombrePropio(ServiceBase):

class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name,times):      
        for i in range(times):
            yield 'Hello, %s' % name


application = Application([HelloWorldService,digitoVerificadorService],
    tns='spyne.examples.hello.soap',
    in_protocol=HttpRpc(),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()


