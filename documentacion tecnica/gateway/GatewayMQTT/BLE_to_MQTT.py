

from gattFunctions import *
import paho.mqtt.client as mqtt
import json
from configparser import ConfigParser
import numpy as np 
import time
import datetime


t_accel=3.0
t_pulso=2.0
miFormato=("%Y-%m-%d %H:%M:%S") #formato de fecha que enviamos en el campo datetime al broker

#funcion que manda los atributos de un dispositivo
def check_device(device): 
    #guardamos en indice la posicion del dispositivo en el array de dispositivos, esta sera igual que el numero
    #de columna en la matriz de temporizadores
    for i in devicesLIST:
        if (i== device):
            indice=devicesLIST.index(i)
            break

    
    #chekeamos los atributos de cada dispositivo uno a uno
    #atributo pulso
    if(time.time()-TIMERS[indice][1]>=t_accel):
        TIMERS[indice][1]=time.time()
        acc_value=get_attribute(device, accUUID, adapter)
        date=datetime.datetime.now()#obtenemos la fecha y hora del aviso
        date=date.strftime(miFormato)
        acc_value['tiempo']=date
        acc_value=json.dumps(acc_value)
        
        miCliente.publish(topic,acc_value)
    if(time.time()-TIMERS[indice][2]>=t_pulso):
        TIMERS[indice][2]=time.time()
        pulso_value=get_attribute(device, pulsoUUID, adapter)
        print(pulso_value)
        if (pulso_value['valor']==0):#lanzamos una alarma si se produce un infarto
            print('alarm()')
        date=datetime.datetime.now()#obtenemos la fecha y hora del aviso
        date=date.strftime(miFormato)
        pulso_value['tiempo']=date
        pulso_value=json.dumps(pulso_value)
        miCliente.publish(topic,pulso_value)
    
#------------------------------INICIALIZACION DEL GATEWAY------------------------------#
#----------recojemos la informacion de configuracion del archivo gateway.conf----------#

parser =ConfigParser()
parser.read('gateway.conf')

devicesDICT = dict(parser['DEVICES'])#almacenamos toda la informacion de dispositivos en un diccionario
devicesLIST = list(devicesDICT.values())#almacenamos toda la informacion en una lista, y la convertimos en tipo lista para poder acceder a sus indices

attribDICT = dict(parser['ATTRIB'])
attribLIST = list(attribDICT.values())

#informacion referente a los atributos 
batteryUUID = parser.get('ATTRIB', 'batteryUUID')
accUUID = parser.get('ATTRIB', 'accUUID')
pulsoUUID = parser.get('ATTRIB', 'pulsoUUID')

#informacion referente al broker mqtt
broker_address = parser.get('BROKER', 'broker_address')
broker_port = int(parser.get('BROKER', 'broker_port'))#convertimos a entero porque por defecto se traen como string
topic= parser.get('BROKER', 'topic')

miCliente=mqtt.Client("cliente1")


#------------------------------NOS CONECTAMOS AL BROKER-------------------------------#
try:
    #commentar lineas 77, 78 y 79 si se quiere permitir la conexion a usuarios anonimos
    username = parser.get('BROKER', 'user')
    password = parser.get('BROKER', 'password')
    miCliente.username_pw_set(username = username, password = password)
    miCliente.connect(broker_address, broker_port)
    print("Conexion con Broker establecida")
except:
    print("Error en la conexion al broker MQTT")

        


#-----------TIMERS QUE CONTROLAN EL POLLING A LOS DISPOSITIVOS-----------#

#definimos el numero de folas y columnas en funcion del numero de timers necesarios
filas = len(devicesLIST) #numero de filas de la matriz
columnas =len(attribLIST)#numero de columnas de la matriz

lista=[] #creamos una lista con el numero total de posiciones de la matriz final
for device in devicesLIST:
    for attrib in attribLIST:
        lista.append(0)        
#https://programacionpython80889555.wordpress.com/2019/09/17/metodo-sencillo-para-crear-matrices-con-python-y-numpy/
#transformamos la lista en una matriz con el numero de columnas y filas
TIMERS=np.array(lista).reshape(filas,columnas)

while True:
    for device in devicesLIST:
        adapter=gatt_init()
        #print(device)
        check_device(device)    
             
       