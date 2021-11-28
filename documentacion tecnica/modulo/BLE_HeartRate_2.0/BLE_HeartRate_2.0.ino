//librerias para el uso de bluetooth
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>

#include<iostream>
#include<cstring>

//libreria para el uso de i2c y libreria del sensor
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"

#define SERVICE_UUID  "6c2422d8-c053-11eb-8529-0242ac130003"
#define CHAR_UUID     "6c242544-c053-11eb-8529-0242ac130003"
#define T_UPDATE      500

BLECharacteristic *pCharacteristic;
bool deviceConnected=false;
int txValue=0;
int blePin=19;
class MyServerCallbacks: public BLEServerCallbacks 
{
  void onConnect (BLEServer* pServer) //callback que se ejecuta cuando se conecta el dispositivo
  {
    digitalWrite(blePin,HIGH);
    deviceConnected =true;
  }
  void onDisconnect(BLEServer* pServer) //callback que se ejecuta cuando se desconecta el dispositivo
  {
    digitalWrite(blePin,LOW);
    deviceConnected =false;
    pServer->getAdvertising()->start();
  }
};
PulseOximeter pox;


unsigned long previousMillis=0;
const long interval=1000;
volatile boolean heartBeatDetected = false;

void onBeatDetected()
{
  heartBeatDetected = true;
}

void setup()
{
  pinMode(blePin,OUTPUT);
  Serial.begin(115200);
  Serial.println("BLE funcionando");
  //-----------------------------SETUP SERVIDOR BLE----------------------------------//
  BLEDevice::init("ERIC_BLE"); //Creamos el dispositivo BLE
  BLEServer *pServer = BLEDevice::createServer(); //creamos un servidor BLE y lo guardamos e un puntero de tipo BLEServicer
  pServer->setCallbacks(new MyServerCallbacks());
  
  BLEService *pService = pServer->createService(SERVICE_UUID); //creamos un servicio con la UUID del servicio y la giardamos en un puntero de tipo service

  //creamos una caracteristica con el UUID de CHAR_UUID y definimos sus propiedades como solo lectura
  pCharacteristic = pService->createCharacteristic(
                                         CHAR_UUID,
                                         BLECharacteristic::PROPERTY_NOTIFY
                                       );
  pCharacteristic->addDescriptor(new BLE2902());//necesario para poder suscribirnos
  pService->start(); //iniciamos el servicio
  
  
  pServer->getAdvertising()->start(); //hacemos que el dispositivo se anuncie
//----------------------SETUP COMUNICACION PULSIOXIMETRO-------------------------//
  // iniciamos el pulsioximetro, si se produce un fallo lo mostramos por pantalla e igual si se consigue conecta
  if (!pox.begin()) 
  {
    Serial.println("Fallo inicio comunicacion pulsioximetro");
    for(;;);
  } 
  else 
  {
    Serial.println("Exito inicio comunicacion pulsioximetro");
  }

 
  pox.setOnBeatDetectedCallback(onBeatDetected);
}

void leerDatos()
{
  uint16_t *stream;
  char dato[10];
  //memset(dato, '-', sizeof(dato+1));
  for(int i=0;i<16;i++)
  {
    dato[i]='-';
  } 

  float bpm = pox.getHeartRate();
  int SpO2 =pox.getSpO2();
  Serial.print("BPM = ");
  Serial.print(bpm);
  Serial.print(" SPO2 = ");
  Serial.println(SpO2);
  String sPulse=String(bpm);
  String sO2=String(SpO2);
  
  String miStr=(sPulse+"-"+sO2);
  int len=miStr.length();
  
  for (int i=0; i<len;i++)
  {
    dato[i]=miStr[i];
    if(i==(len-1))
    {
      i++;
      for (i; i<10;i++)
        dato[i]='\0';
    }
  }
  pCharacteristic->setValue(dato); //damos el valor a la caracteristica
  pCharacteristic->notify();
  //Serial.print("Sent value" + String(dato));*/
}

void loop()
{
  pox.update();
  
  unsigned long currentMillis=millis();
  if(currentMillis-previousMillis>=interval)
  {
    pox.shutdown();
    leerDatos();
    pox.resume();
    previousMillis=currentMillis;
  }
}
