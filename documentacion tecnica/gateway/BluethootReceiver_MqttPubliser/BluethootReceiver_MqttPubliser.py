import sys #libreria para interactuar con el sistema
import paho.mqtt.client as mqtt #libreria para crear un cliente mqtt
import json #importamos la libreria para usar json

def publish(client): #callback que se ejecuta cuando recibimos un mensaje

    miMensaje =str(message.payload.decode("utf-8"))
    print("Mensaje recibido =", miMensaje) #decodificamos la informacion recibida a formato utf8, lo convertimos a string y lo almacenamos en miMensaje)
    #print("Topic", message.topic)
    #print("QoS=", message.qos)
    
    

#----------------------------------------------------------------CLIENTE MQTT----------------------------------------------------------------#

broker_address ="192.168.250.60"
borker_port =1883
topic = "topic"
miCliente = mqtt.Client("raspi")

#if (allow anonimous == false)    
miCliente.username_pw_set(username="user1",password="pass1") #introducimos nombre y contrasseña para conectarnos (solo para la raspberry)
miCliente.connect(broker_address, borker_port)
mensaje = json.dumps({"idDispositivo": 'C0:50:03:32:1F:33', "tipoDato": "pulso", "valor": 100,  "tiempo":"2020-12-20 15:25:50"})

print(mensaje)
miCliente.publish(topic,mensaje)

