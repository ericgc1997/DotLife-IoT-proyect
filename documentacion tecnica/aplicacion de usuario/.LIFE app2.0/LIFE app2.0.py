import matplotlib.pyplot as plt
import matplotlib
from numpy import random
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

import matplotlib.dates as mdates

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock




import datetime as dt
import socket
import pickle   #para poder convertir en objetos la informacion recivida en forma de bytes a traves de socket


def get_Pulse_Value(device):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('54.195.171.207', 2909)) #nos conectamos al servidor

    HEADERSIZE=30

    s.send(device.encode())
    complete_info=b''

    while True:
        #variable en la que guardaremos el mensaje que llegue del servidor, indicamos que seran bytes
        msg=s.recv(8) #recibimos mensajes de 8 bytes
        if len(msg)<=0: #cuando la longitud del mensaje recivido es 0 salimos del bucle
            break
        #complete_info+= msg.decode('utf-8') #decodificamos el mensaje que ha sido recibido y lo vamos guardando en  otra variable
        complete_info+= msg #guardamos el mensaje conforme va siendo recivido
    
    tupla=pickle.loads(complete_info[HEADERSIZE:])
    return(tupla)

def funcPrueva():
    tupla=(random.rand(), random.rand() ,16)
    return tupla


fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
plt.title(label='CONSTANTES VITALES PACIENTE', fontsize=60, color="green")
plt.xlabel("Fecha", fontsize=15, color='white')

plt.grid(color='grey')
canvas = fig.canvas
#plt.plot([1, 23, 2, 4])
#plt.ylabel('some numbers')

class MyApp(App):
    
    
    
    def build(self):
        box = BoxLayout(orientation='vertical') #box define todo el espacion en pantalla
        self.i = 0 #valor inicial
        self.pArr = [self.i] #valor inicial array pulso
        self.oArr=[self.i] #valor inicial array saturacion o2
        self.tArr= ['0'] #valor inicial array tiempo
        self.oldTupla={}
        titulo=Button(text="COSNTANTES DE ERIC" ,size_hint=(1, 0.1), color=('white'), pos=(0,100))
        box.add_widget(titulo)

        box.add_widget(canvas)
        
        Clock.schedule_interval(self.update, 0.5)
        return box

    def update(self, *args):
        
        
        Tupla=get_Pulse_Value('A8032A6A4FAA')
        if (Tupla==self.oldTupla):
            pass
        else:

            #Tupla=funcPrueva()
            #self.i = Tupla[0] #valor actualizado
            self.pArr.append(Tupla[0])
            self.oArr.append(Tupla[1])
            self.tArr.append(str(len(self.tArr)+1))
            
            
            ax = plt.gca() #obtenemos lo ejes
            ax.xaxis.set_major_locator(plt.MaxNLocator(10))#indicamos el numero maximo de labels en el eje x
            ax.set_facecolor((0, 0, 0)) #indicamos el color de fondo donde se muestran las graficas
            
            ax.tick_params(axis='x', colors='white')  #indicamos el color de fondo del eje x
            ax.tick_params(axis='y', colors='white')  #indicamos el color de fondo del eje y
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            
            
            
            #matplotlib.rcParams = 'your_color'
            #text.color = 'your_color'
            
            plt.plot(self.tArr, self.pArr, marker='o', markersize=5, color='red', linewidth=5, label='Pulso'if self.i == 0 else "")
            plt.plot(self.tArr, self.oArr, marker='o', markersize=5, color='blue', linewidth=5, label='Saturación'if self.i == 0 else "")
            self.i=1
            plt.legend()
                
            canvas.draw_idle()
            self.oldTupla=Tupla
            #Axis.set_major_locator(xaxis, 10) 
            #canvas.draw_idle()
    
        
        
        
MyApp().run()