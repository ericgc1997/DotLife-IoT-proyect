import pygatt
# from datetime import datetime
import time
from datetime import datetime


device1="C0:50:03:32:1F:33"
batteryUUID= "00020000-0001-11e1-ac36-0002a5d5c51b"
accUUID="00800000-0001-11e1-ac36-0002a5d5c51b"
pulsoUUID="29091997"
result={}

def gatt_init():
    adapter = pygatt.GATTToolBackend() #habilitamos es uso de codigo de backend gatt
    return adapter


def battery_handle(handle, value):#callback que procesa la informacion de un atributo de tipo bateria
    time.sleep(0.001) #esperamos un milisegundo, de otro modo la informacion no se recive adecuadamente
    value.reverse()#convertimos de litle endian que es como viene la informacion a big endian
    value=list(value) #convertimos los valores de entrada en tipo lista, pues se reciven como bytearray
    #concatenamos los bytes 7 y 8 que corresponden al timestamp y lo convertimos en entero
    timestamp=int(str(value[6])+str(value[7]))
    #concatenamos los bytes 4 y 5 y lo adaptamos (segun datasheet) para obtener el% de bateria
    battery=int(str(value[4])+str(value[5]))*10
    global result
    result={'timestamp':timestamp, 'battery':battery}
    

#callback que procesa la informacion de un atributo de tipo bateria y
#añade a un dicionario global un diccionario con los valores x, y, z
def acc_handle(handle, value):
    
    time.sleep(0.001) #esperamos un milisegundo, de otro modo la informacion no se recive adecuadamente
    
    value.reverse()
    value=list(value) #comvertimos los valores de entrada en tipo lista, pues se reciven como bytearray

    timestamp=int(str(value[6])+str(value[7]))
    xAxis=int(value[4])+int(value[5])
    yAxis=int(value[2])+int(value[3])
    zAxis=int(value[0])+int(value[1])
    #guardamos la informacion el un dicionario   
    value={'x':xAxis, 'y':yAxis, 'z':zAxis}
    
    #añadimos a la variable global el resultado 
    global result
    result.update(value)



def get_attribute(dev, attrib, adapter):
    #intentamos conectarnos y suscribirnos a un atributo, al recibir la informacion,salimos del bucle
    #el bucle sirve para mantenerse dentro del try hasta que recibimos la informacion

    while True:  
        try:
            adapter.start()#iniciamos el adaptador bluetooth(hci0)
            device = adapter.connect(dev) #nos conectamos al dispositivo
            global result
            result={'idDispositivo':dev} #indicamos en el resultado que vamos a devolver, el dispositivo que manda el mensaje
            if (attrib==batteryUUID): #atributo bateria
                device.subscribe(batteryUUID,callback=battery_handle)
                now=datetime.now()
                now=now.strftime("%Y/-%m-%d %H:%M:%S")
                result.update({"tiempo":now})
            elif(attrib==accUUID):  #atributo aceleracion  
                device.subscribe(accUUID, callback= acc_handle)
                now=datetime.now()
                now=now.strftime("%Y/-%m-%d %H:%M:%S")
                result.update({"tiempo":now})
            elif(attrib==pulsoUUID): #atributo pulso
                #device.subscribe(accUUID, callback= acc_handle)
                now=datetime.now()
                now=now.strftime("%Y/-%m-%d %H:%M:%S")
                result=({'tipoDato': 'pulso', 'valor': 62})
                result.update({'tiempo':now})
            else:#en caso de que el atributo seleccionado no exista devolvemos un diccionario vacio
                print("Selected attribute do not exist")
                time.sleep(5)
                result={}
                
            time.sleep(0.1)#esperamos 100 ms para
            break
        except:
            print("Fallo en la conexion bluetooht")
        finally:   
            adapter.stop()#finalizamos la conexion con la interfaz bl
            return result
            #meter aqui el script para resetear el hci0

   

