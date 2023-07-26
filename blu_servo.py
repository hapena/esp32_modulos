from machine import Pin, PWM
import bluetooth
from BLE import BLEUART
import utime


name= "EspRobot"

print (name, "Verificando  ok")

ble = bluetooth.BLE()
uart = BLEUART(ble, name)

servo = PWM(Pin(8), freq=50)

def map(x):
        return int((x - 0) * (125-25) / (180 - 0) + 25)
    

def on_rx():    
    rx_recibe = uart.read().decode().strip()
    uart.write("EspRobot dice: " + str(rx_recibe) + "\n")
    print(rx_recibe)
    
    if rx_recibe == "!B516":
        
        m = map(0)
        servo.duty(m)
        
    if rx_recibe == "90":
        
        m = map(90)
        servo.duty(m)
        
    if rx_recibe == "180":
        
        m = map(180)
        servo.duty(m)
        
        
        
    
    
uart.irq(handler = on_rx)

