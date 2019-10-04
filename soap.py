
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
from spyne.model.primitive import Boolean, Unicode, Integer
from spyne.model.complex import ComplexModel

class MyHeader(ComplexModel):
   info = Unicode

class digitoVerificadorService(ServiceBase):
    __in_header__ = MyHeader

    @rpc(Unicode,Integer, _returns = Iterable(Unicode))
    def digito_verificador(ctx,rut,times):
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
                    msg = 'El rut ingresado ' + rut + ' es valido y tiene como digito verificador ' + completeRut[1]
                    yield msg
            else:
                msg = 'El rut ingresado ' + rut + ' es invalido o el formato esta errado'

class nombrePropioService(ServiceBase):
    __in_header__ = MyHeader

    @rpc(Unicode,Unicode,Unicode,Unicode, _returns = Iterable(Unicode))
    def nombre_propio(ctx,name,apellidop,apellidom,gender):

        if gender=='M':
            gender='Sr.'
        elif gender=='F':
            gender='Sra.'
        nombreCompleto = gender + ' ' + name + ' ' + apellidop + ' ' + apellidom
        msg = 'Hola ' + nombreCompleto.title()
        yield msg


class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name,times):      
        for i in range(times):
            yield 'Hello, %s' % name

application = Application([
        HelloWorldService,
        digitoVerificadorService,
        nombrePropioService
    ],
    tns='/',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()


