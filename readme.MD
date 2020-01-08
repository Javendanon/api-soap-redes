# API SOAP REDES

Api soap basada en python 2.7 debido a la incompatibilidad de las librerías utilizadas 

# Install

Para instalar se debe hacer un entorno virtual con una versión de [Python 2.7.16](https://www.python.org/downloads/release/python-2716/) , agregar a PATH las variables de python2, y posteriormente ejecutar los siguiente comando en consola

```
pip install spyne
pip install lxml
```

## Ejecución
Para levantar la API soap se debe ejecutar el siguiente comando desde la terminal en el directorio del repositorio
```
python2 soap.py
```
siendo python2 la variable de entorno PATH de python 2.7.16 (puede ser nombrada de otra forma)

y esperar a que cargue, posteriormente en la consola se imprimirá una dirección de tipo 

`http://localhost:puerto`

el puerto puede variar dependiendo del equipo, la api se compone de 2 métodos 

el archivo wsdl con los servicios puede ser encontrado en

`http://localhost:puerto/?wsdl`


### VerificaRut 
Servicio POST que calcula y verifica el rut ingresado de tipo "12345678-9", responde en formato XML y retorna un mensaje al cliente con la información. Se recomienda utilizar SoapUI para realizar las peticiones a la API cargando el archivo wsdl
Este servicio contiene 1 atributo unicode

`rut`

### NombrePropio

Servicio POST que aplica formato proper case el nombre, apellido materno, apellido paterno y género que sea ingresado independiente del formato inicial, responde en formato XML y retorna un mensaje al cliente con la información. Se recomienda utilizar SoapUI para realizar las peticiones a la API cargando el archivo wsdl 


Este servicio contiene 4 atributos unicode 
```
name
apellidop
apellidom
gender
```

Para realizar las peticiones HTTP correspondientes se debe utilizar protocólo Soap11, por ende es más fácil realizarlo mediante SoapUI y el archivo wsdl o el cliente proporcionado por los estudiantes que desarrollaron las API