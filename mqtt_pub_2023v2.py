from machine import Pin, ADC
from utime import sleep, sleep_ms
from dht import DHT11
import ujson
from umqtt.simple import MQTTClient
import network, time, urequests

s_dht= DHT11(Pin(2))

# MQTT Server Parameters
MQTT_CLIENT_ID = "hugo1234567890"
MQTT_BROKER    = "broker.hivemq.com"
#MQTT_BROKER    = "192.168.20.25"  #  en docker apuntar al host local
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "andina/python/noche"

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


#if conectaWifi ("Claro_6683E8", "EeX/Stt3w4NQr9ColQI/fQ=="):
if conectaWifi ("Hugo", "Hupe6493"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())


    print("Conectando a  MQTT server... ",MQTT_BROKER,"...", end="")
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    client.connect()

    print("Conectado!")

    

    while True:
        s_dht.measure()
        tem = s_dht.temperature()
        hum = s_dht.humidity()
        print("T:{} c   H:{}% ".format(tem,hum))
        sleep_ms(50)


        print("Revisando Condiciones ...... ")
        message = ujson.dumps({
        "Humedad": hum,
        "Temperatura": tem,
        })

        
            
        print("Reportando a  MQTT topic {}: {}".format(MQTT_TOPIC, message))
        client.publish(MQTT_TOPIC, message)
        nuevo_dato = message

        
        time.sleep(3)


else:
       print ("Imposible conectar")
       miRed.active (False)