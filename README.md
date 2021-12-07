# DotLife-IoT-proyect
#### 6/2021 Eric Garcia
Vertical IoT solution: From sensor data reading up to the user interface.

```bash
│   .gitignore
│
├───Canvas modelo de negocio y presentacion
│       Explicación modelo de negocio y business model canvas.pdf
│       plan de negocio.xlsx
│       Presentación proyecto.pptx
│
├───documentacion tecnica
│   │   Documentacion funcional.pdf
│   │   documentacion tecnica de la solucion.pdf
│   │
│   ├───aplicacion de usuario
│   │   └───.LIFE app2.0
│   │           LIFE app2.0.py
│   │
│   ├───bibliografia
│   │
│   ├───gateway
│   │   ├───BluethootReceiver_MqttPubliser
│   │   │       BluethootReceiver_MqttPubliser.py
│   │   │
│   │   └───GatewayMQTT
│   │       │   BLE_to_MQTT.py
│   │       │   gateway.conf
│   │       │   gattFunctions.py
│   │       │   readme
│   │       │
│   │       └───__pycache__
│   │
│   ├───modulo
│   │   └───BLE_HeartRate_2.0
│   │           BLE_HeartRate_2.0.ino
│   │
│   └───servidor
│       │   aws iot machine key.ppk
│       │   DB_pulsioximetro.sql
│       │   DB_pulsioximetro2.sql
│       │   pardeclavesservidoriot.pem
│       │
│       └───Scripts
│           ├───MqttSuscriber_DbInserter
│           │       config.txt
│           │       MqttSuscriber_DbInserter2.0.py
│           │
│           └───Server_socket
│                   Server_socket.py
│                   socket.conf.txt
│
└───pictures
```

(Please keep in mind that some of the documentation files are writen in spanish)  
- Canvas modelo de negocio y presentación: Information regarding a possible business model based on the technical solution presented.   
- Documentación funcional.pdf: file explaining the reason to chose each one of the tools used in the solution 
- documentación técnica de la solución.pdf: file explaining the steps needed to develope this project
- aplicación de usuario: App que muestra al usuario una interfaz con los datos procedentes del servidor.   
- gateway: BLE and MQTT managing scripts for a gateway  
- BluethootReceiver_MqttPubliser: scripts to manage BLE devices data receiving (polling) and data sending to a MQTT broker
- GatewayMQTT: MQTT Broker that manage the infromation receibed in the local Broker to the cloud Broker (MQTT Bridge)
- Módulo: .ino Files that configure and manage an i2c pulse-oximeter, and send this information to a BLE receiver .    
- DB_pulsioxímetro2: data base.  
- Scripts.:  scripts in head od data transmision from and to the server.
- MqttSuscriber_DbInserter.: Script that receives the broker information and stores it appropriately in the database.  
- Server_socket: Script that creates a comunication socket to trasfer data form the database to the user application and vice versa


<p align="center">
  <img src="https://github.com/ericgc1997/DotLife-IoT-proyect/blob/master/pictures/Network%20scheme.png">  
  <p align="center"> communication scheme</p>  
</p>  
<p align="center">
  <img src="https://github.com/ericgc1997/DotLife-IoT-proyect/blob/master/pictures/ejemplo%20aplicacion%20de%20usuario.png" width= "470" height="300">
  <p align="center"> user Application</p>  
</p>  
<p align="center">
  <img src="https://github.com/ericgc1997/DotLife-IoT-proyect/blob/master/pictures/comunnication%20app.png" width= "450"height="300">
  <p align="center"> Server-Application communication</p>  
</p>  
