
import mariadb #libreria para usar la base de datos
import sys #libreria para interactuar con el sistema

import paho.mqtt.client as mqtt #libreria para crear un cliente mqtt
import json #importamos la libreria para usar json

from configparser import ConfigParser
#from termcolor import colored

infarto=0

#funcion que interactua con una base de datos en funcion del string de entrada
def message_to_db(miMensaje , cursor):
    # Insertamos en la base de datos en funcion del tipo de dato, los tipos de datos son 
    # {"idDispositivo": nº, "tipoDato": "pulso", bpm:101,15 "so2": 98, "tiempo":'2020-12-20 15:25:50'} para los mensajes que mandan pulso
    global infarto
    if("tipoDato"in miMensaje):
        if('idDispositivo'in miMensaje):
            idDispositivo= miMensaje['idDispositivo'] #guardamos en la variable idDispositivo el valor del campo correspondiente por ejemplo C0:50:03:32:1F:33
            idDispositivo =idDispositivo.replace(':','') #eliminamos los ':' que separa cada par de numeros hexadecimales para guardarlo en la base de datos  
        try:#insertamos en la base de datos en funcion de la informacion del JSON de entrada
            #es imperativo usar STR_TO_DATE para indicar cual es el formato de entrada de la fecha a la base de datos
            if(miMensaje["tipoDato"]=="pulso"):
                cursor.execute('INSERT INTO {}(ID_Dispositivo, Pulso, O2, Tiempo) VALUES("{}",{}, {}, STR_TO_DATE("{}","%Y-%m-%d %H:%i:%s"))'.format(tablaPulso,idDispositivo, miMensaje["bpm"], miMensaje["so2"], miMensaje["tiempo"]))
                
                if (miMensaje['bpm']==0 and infarto==0):
                    cursor.execute('INSERT INTO {}(ID_Dispositivo, infarto, Fecha) VALUES("{}",{}, STR_TO_DATE("{}","%Y-%m-%d %H:%i:%s"))'.format(tablaAnomalias,idDispositivo, 1, miMensaje["tiempo"]))    
                    infarto=1
                elif(miMensaje['bpm']!=0):
                    infarto=0
            else:
                print("El tipo de dato no tiene la informacion adecuada para ser almacenado")
            
            conn.commit()
        except mariadb.Error as e:
            print(e)


def on_message(client, userdata, message): #callback que se ejecuta cuando recibimos un mensaje
    
    miMensaje =str(message.payload.decode("utf-8","ignore")) #decodificamos la informacion recibida a formato utf8
    #print("Topic", message.topic)
    #print("QoS=", message.qos)

    try:
        miMensaje=json.loads(miMensaje)#codificamos de JSON a un python object
        print(miMensaje)
    except json.JSONDecodeError as e:
        print("fallo en la decodificacion del JSON de entrada:{}".format(e))
    message_to_db(miMensaje, cur) #llamamos a la funcion de escritura en la base de datos



#-------------------------------------LECTURA DE LOS PARAMETROS DE CONEXION AL BROKER Y LA BASE DE DATOS-------------------------------------#

parser=ConfigParser()
try: #lectura de los parametros de configuracion desde el fichero
    parser.read('config.txt')
    dbUser= parser.get('DB','user')
    dbPassword= parser.get('DB','password')
    dbHost= parser.get('DB','host')
    dbPort= int(parser.get('DB','port'))#como por defecto se traen los archivos como string lo convertimos a entero
    database=parser.get('DB','database')

    broker_address= parser.get('BROKER','broker_address')
    borker_port= int(parser.get('BROKER','borker_port'))#como por defecto se traen los archivos como string lo convertimos a entero
    topic = parser.get('BROKER','topic')
    broker_username=parser.get('BROKER','broker_username')
    broker_password=parser.get('BROKER','broker_password')
except :
    print("Se ha producido un error en la lectura de los ficheros")





#----------------------------------------------------INTERRACCION CONTRA LA BASE DE DATOS----------------------------------------------------#
#Parametros de conexion con la base de datos
#intentamos establecer la conexion con los parametros especificados

#nombres tablas
tablaPulso="pulso"
tablaO2="saturacion"
tablaUsuarios="usuarios"
tablaAnomalias="anomalias"

try:
    print("Conectando a la base de Datos...")
    conn =mariadb.connect(
        user=dbUser,
        password=dbPassword,
        host=dbHost,
        port=dbPort,
        database=database
    )
except mariadb.Error as bd: #En caso de que falle la conexion con los parametros especificados lo mostramos por pantalla
    print("Erroc conectando a la base de datos: {}".format(bd))
    sys.exit(1) #finalizamos el script con el codigo de error 1

print("Conectado a la Base de Datos")

#creamos el objeto cur (cursor) que nos permitira realizar las instrucciones contra la DB
cur =conn.cursor()

    
#----------------------------------------------------------------CLIENTE MQTT----------------------------------------------------------------#
try:
    print("Conectando al Broker...")
    miCliente = mqtt.Client("CLIENT")
    
    miCliente.on_message = on_message
    #if (allow anonimous == false)    
    miCliente.username_pw_set(username=broker_username,password=broker_password) #introducimos nombre y contrasseña para conectarnos (solo para la raspberry)


    miCliente.connect(broker_address, borker_port)
    print("Conectado al Broker")
    
    miCliente.subscribe(topic) #nos suscribimos al topic
    print('Subscrito al topic "{}"'.format(topic))
    miCliente.loop_forever()  #inicio del bucle
except:
    print("Fallo en la conexion con el broker:")
    print("IP: {}\nPuerto: {}\nUsuario: {}".format(broker_address,borker_port,broker_username))