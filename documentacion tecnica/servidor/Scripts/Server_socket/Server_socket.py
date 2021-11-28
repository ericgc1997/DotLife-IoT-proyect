import mysql.connector #para interactuar con una base de datos
import socket   #para establecer una conexion por socket
import pickle   #para poder enviar objetos a traves de socket
from configparser import ConfigParser #para leer archivos (fichero de coniguracion)



#-------------------------------------LECTURA DE LOS PARAMETROS DE CONEXION AL BROKER Y LA BASE DE DATOS-------------------------------------#
parser=ConfigParser()
try: #lectura de los parametros de configuracion desde el fichero
    parser.read('socket.conf.txt')
    
    dbUser= parser.get('DB','user')
    dbPassword= parser.get('DB','password')
    dbHost= parser.get('DB','host')
    dbPort= int(parser.get('DB','port'))#como por defecto se traen los archivos como string lo convertimos a entero
    database=parser.get('DB','database')

    headerSize= int(parser.get('SOCKET','headerSize'))
    sk_port= int(parser.get('SOCKET','port'))#como por defecto se traen los archivos como string lo convertimos a entero
    client_address = parser.get('SOCKET','client_address')
    
except:
    print("Se ha producido un error en la lectura de los ficheros")


#--------------------------ESTABLECIMIENTO CONEXION BASE DE DATOS-------------------------------------------------#

#funcion que recoje el ultimo row de la table pulso devuelve la fecha en formato %Y, %M, %d, %H, %m, %s
def get_Last_Pulse_Row(dispositivo , cursor):
    cursor.execute("SELECT Pulso, O2, Tiempo FROM pulso WHERE ID_Dispositivo ='{}' ORDER BY Tiempo DESC LIMIT 1".format(dispositivo))#cojemos el ultimo valor de la tabla de la base de datos
    lst = cursor.fetchall()#guardamos el resultado en una variable
    conn.commit()#cerramos la conexion
    if not lst: #si la respuesta a la consulta esta vacia
        return lst #devolvemos el resultado vacio
    else: #si la consulta tiene algun resultado 
        return lst[0] #obtenemos el primer y unico elemento de la consulta

def get_Owner_Device(nombre, cursor):
    cursor.execute("SELECT ID_Dispositivo FROM usuarios WHERE Nombre ='{}'".format(nombre))
    name=cursor.fetchall()
    conn.commit()
    name=str(name[0])
    name=name[2:14]
    return name
try:
    print("Conectando a la base de Datos...")
    conn =mysql.connector.connect(
        user=dbUser,
        password=dbPassword,
        host=dbHost,
        port=dbPort,
        database=database   
    )

except: #En caso de que falle la conexion con los parametros especificados lo mostramos por pantalla
    print("Erroc conectando a la base de datos")
print("Conectado a la Base de Datos")




#--------------------------ESTABLECIMIENTO DE LA COMUNICACION POR SOCKET-------------------------------------------------#


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET=IPV4, SOCK_STREAM=TCP indicaos el tipo de socket
s.bind(('',sk_port))# enlazamos la conexion con el cliente
s.listen(5) #escuchamos indicando un numero maximo de conexiones simultaneas de 5

HEADERSIZE=headerSize

while True: #mientras la conexion este establecida
    client, adr=s.accept() #aceptamos la conexion
    received=client.recv(1024).decode()

    if not received:#si no recibimos datos cerramos la conexion
        print("no hay datos")
        client.close()
        break
    else:#si recibimos datos
        cur=conn.cursor()#creamos un cursor para hacer una consulta a la base de datos
        print(received)
        #buscamos el ultimo valor del pulso de la base de datos del dispositivo indicado por el cliente                                        
        #y guardamos en una tupla el resultado de la consulta a la base de datos
        
        if(received[:1]=='N'):#si la primera letra enviada es N ejecutamos una funcion (el mensaje es de alexa)
            name= get_Owner_Device(received[1:] , cur)
            print(name)
            tupla=get_Last_Pulse_Row(name , cur)
            print(tupla)
        else:#sino el mensaje es de la applicacion
            tupla=get_Last_Pulse_Row(received , cur)

        print("Connexion con {} establecida".format(adr))
        
        sendMsg=pickle.dumps(tupla) #convertimos la tupla en un string de bytes para poder ser enviado
        #convertimos en un stream de bytes del tamaño del mensaje mas una cabezera de seguridad 
        #sendMsg=bytes(f'{len(sendMsg):<{HEADERSIZE}}','utf-8')+ sendMsg 
        
        sendMsg=bytes(f'{len(sendMsg):<{HEADERSIZE}}','utf-8')+ sendMsg 
        client.send(sendMsg)#enviamos el mensaje en forma de bytes
        client.close()
