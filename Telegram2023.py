import network, time, urequests
from machine import Pin, ADC
from utelegram import Bot

TOKEN = '5031163680:AAG45iFduorhunFrZs6GsGGBc7QUaegYGhE'

rojo= Pin(2, Pin.OUT)
verde= Pin(4, Pin.OUT)

bot = Bot(TOKEN)

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

if conectaWifi ("Wokwi-GUEST", ""):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())

    @bot.add_message_handler('inicio')
    def help(update):
        update.reply('''Menu:  
                      \n   encender led verde : verde on   \U0001F601
                      \n   apagar led verde : verde off
                      \n   encender led verde : rojo on
                      \n   apagar led verde : rojo  off
                      ''')

    @bot.add_message_handler('verde on')
    def help(update):
        verde.value(1)
        update.reply('Verde encendido')

    @bot.add_message_handler('verde off')
    def help(update):
        verde.value(0)
        update.reply('Verde apagado')
    
    @bot.add_message_handler('rojo on')
    def help(update):
        rojo.value(1)
        update.reply('Rojo encendido')

    @bot.add_message_handler('rojo off')
    def help(update):
        rojo.value(0)
        update.reply('Rojo apagado')

    
    
    
    bot.start_loop()

else:
       print ("Imposible conectar")
       miRed.active (False)