# DotLife-IoT-proyect
Solución IoT Vertical: Desde la lectura de datos de un sensor, hasta la aplicación de usuario.

**->Canvas modelo de negocio y presentación**    --Informacion relativa a un posible modelo de negocio basado en la solución 
tecnica expuesta.  

**->documentación técnica**  
&nbsp;&nbsp;&nbsp;**->Documentación funcional.pdf**  
&nbsp;&nbsp;&nbsp;**->documentación técnica de la solución.pdf**   
&nbsp;&nbsp;&nbsp;**->aplicación de usuario** --App que muestra al usuario una interfaz con los datos procedentes del servidor.   
&nbsp;&nbsp;&nbsp;**->gateway**   --scripts que se encargan de gestionar un gateway BLE a MQTT.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**->BluethootReceiver_MqttPubliser.** --script que se conecta con diversos dispositivos BLE (polling) y envia sus datos a un broker MQTT local  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**->GatewayMQTT.** --Broker MQTT que envia la informacion recivida en el Broker local a otro broker MQTT en la nube (MQTT Bridge)   
&nbsp;&nbsp;&nbsp;**->módulo**  -- archivos .ino que configuran y gestionan un pulsioximetro i2c crean un UUID BLE y envia esta informacion a un receptor BLE que se conecte a este.   
&nbsp;&nbsp;&nbsp;**->servidor.**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**->DB_pulsioxímetro2**  --Base de datos.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**->Scripts.**   --scripts que se encargan del envio y recepcion de información  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**->MqttSuscriber_DbInserter.** -- Script que recive la información del broker y la guarda adecuadamente en la base de datos.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**->Server_socket.**   --Script que crea un socket de comunicación con la aplicacion de usuario y envia los datos solicitados por la aplicacion.  
