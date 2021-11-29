# DotLife-IoT-proyect
#### 6/2021 Eric Garcia
Solución IoT Vertical: Desde la lectura de datos de un sensor, hasta la aplicación de usuario.

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


Canvas modelo de negocio y presentación**    --Informacion relativa a un posible modelo de negocio basado en la solución 
tecnica expuesta.  

- Documentación funcional.pdf: archivo en el que se explica el porque se ha elegido cada una de las herramientas
- documentación técnica de la solución.pdf: archivo en el que se explica paso a paso como se ha realizado el proyecto
- aplicación de usuario: App que muestra al usuario una interfaz con los datos procedentes del servidor.   
- gateway: scripts que se encargan de gestionar un gateway BLE a MQTT.  
- BluethootReceiver_MqttPubliser: script que se conecta con diversos dispositivos BLE (polling) y envia sus datos a un broker MQTT local  
- GatewayMQTT: Broker MQTT que envia la informacion recibida en el Broker local a otro broker MQTT en la nube (MQTT Bridge)   
- Módulo: Archivos .ino que configuran y gestionan un pulsioximetro i2c crean un UUID BLE y envia esta informacion a un receptor BLE que se conecte a este.   
servidor. 
- DB_pulsioxímetro2: Base de datos.  
- Scripts.: scripts que se encargan del envio y recepcion de información  
- MqttSuscriber_DbInserter.: Script que recibe la información del broker y la guarda adecuadamente en la base de datos.  
- Server_socket: Script que crea un socket de comunicación con la aplicacion de usuario y envia los datos solicitados por la aplicacion.  

