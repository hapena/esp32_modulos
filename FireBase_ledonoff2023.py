#------------------------------ [IMPORT]------------------------------------


import network, time, urequests
from machine import Pin, ADC, PWM
import utime
import ujson
import ufirebase as firebase

#--------------------------- [OBJETOS]---------------------------------------
led = Pin(2, Pin.OUT)


#----------------------[ CONECTAR WIFI ]---------------------------------------------------------#

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

    

#------------------------------------[BOT]---------------------------------------------------------------------#

if conectaWifi ("Wokwi-GUEST", ""):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
    firebase.setURL("https://iot-andina-default-rtdb.firebaseio.com/")
    
    

    while True:

      message = led.value()

      #Put 
      firebase.put("Led", message, bg=0)
      print("Enviado...", message)
      

      #Get 
      firebase.get("Led", "dato_recuperado", bg=0)
      print("Recuperado.... "+str(firebase.dato_recuperado))
      
      if firebase.dato_recuperado == 0:
        led.value(1)
        print("led on")
      
      else:
        led.value(0)
        print("led off")
      
      
      

else:
       print ("Imposible conectar")
       miRed.active (False)