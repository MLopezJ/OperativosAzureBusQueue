"""
Antes de compilar, asegurarse de ejecutar primeramente el archivo arduino y subirlo a memoria
en el mismo. Despues de eso, ejecutar este archivo.

El interruptor se podia haber hecho con un bool, pero se queria practicar con diccionarios.
"""

#imports
from azure.servicebus import ServiceBusService, Message
import random
import serial, string
from time import sleep, time
from datetime import datetime

#globals
bus_service = ServiceBusService(
    service_namespace='service-bus-queue',
    shared_access_key_name='RootManageSharedAccessKey',
    shared_access_key_value='2JoqjrWyYZMOnHGtFBhtPDfGhauso3y0krQGqA0PpSw=')

interruptor = {'apagado': '24866484853536557575454493'}

#methods 
def insertarEnServiceBus(cantidadDeInserciones):
    print("cantidad de inserciones a realizar: ", cantidadDeInserciones)
    var=cantidadDeInserciones
    while (var>0):
        tiquete= random.randint(0,5)
        msg=Message(str(tiquete))
        bus_service.send_queue_message('queue_so', msg)
        var-=1

def activarAzure():
    arduino = serial.Serial('/dev/ttyACM0',9600, 8,'N',1,timeout=1)
    print("esperando interaccion...")
    rfidReader = ""
    while True:
        while(rfidReader != ''):
            if(rfidReader in interruptor.values()):
                if(interruptor.keys()[interruptor.values().index(rfidReader)] == 'apagado'):
                    cantSegundos = 0
                    inicioTiempo = datetime.now()
                    print("empezar cronometro")
                    interruptor['encendido'] = interruptor.pop('apagado')
                    rfidReader = ""
                elif(interruptor.keys()[interruptor.values().index(rfidReader)] == 'encendido'):
                    finTiempo = datetime.now()
                    print("apagar cronometro")
                    interruptor['apagado'] = interruptor.pop('encendido')
                    rfidReader = ""
                    
                    cantTiempo = finTiempo - inicioTiempo
                    cantSegundos = cantTiempo.seconds
                    print("cantidad de segundos: ", cantSegundos)
                    
                    insertarEnServiceBus(cantSegundos)    
                    
        rfidReader = arduino.readline()
    arduino.close()
            
    
activarAzure()


