import network, time, urequests
from machine import Pin
from utime import sleep, sleep_ms, ticks_us
from dht import DHT11
import ujson
import ufirebase as firebase

s_dht= DHT11(Pin(2))

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


if conectaWifi("Claro_6683E8", "EeX/Stt3w4NQr9ColQI/fQ=="):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
    firebase.setURL("https://iot-andina-default-rtdb.firebaseio.com/")
    
   
    
    while True:
        
        s_dht.measure()
        tem = s_dht.temperature()
        hum = s_dht.humidity()
        print("T:{} c   H:{}% ".format(tem,hum))
        sleep_ms(50)
              
        #message={"Nombre": "hugo", "Edad": 18. "CC": 1030666777}

        message={"Temperatura": tem, "Humedad": hum}

        #Put Tag2
        firebase.put("andina/diplomado",message, bg=0)
        print("dato enviado")
        
        #Get Tag2
        firebase.get("andina/diplomado", "dato", bg=0)
        print("Dato recuperado: "+ str(firebase.dato))
        
        #Put Tag2
        #firebase.put("cisco/jgc/tarde/{}".format(ticks_us()),message, bg=0)
        #print("dato enviado")
    
        #firebase.get("cisco/jgc/tarde/{}".format(ticks_us()), "dato_recuperado", bg=0)
        #print("Recuperado.... "+str(firebase.dato_recuperado)," ", valor )

    
 
else:
       print ("Imposible conectar")
       miRed.active (False)

