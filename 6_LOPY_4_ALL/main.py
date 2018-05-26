import machine
import pycom
import time
from machine import Pin
from network import LoRa
import socket
from network import Bluetooth
from network import WLAN
import network

pycom.heartbeat(False)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:

        print('wake form deepsleep')
        time.sleep(1)

bluetooth = Bluetooth()
wlan = network.WLAN(mode=network.WLAN.STA)
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

def conn_cb (bt_o):
    events = bt_o.events()
    if  events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")


bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)


#BLE

bluetooth.deinit()
wlan.deinit()
lora.power_mode(LoRa.SLEEP)

bluetooth = Bluetooth()
pycom.heartbeat(False)
pycom.rgbled(0x000077)

print('sending BT')
bluetooth.set_advertisement(name='LoPy', service_uuid=b'1234567890abcdef')
bluetooth.advertise(True)

time.sleep(8)

#micro
bluetooth.deinit()
wlan.deinit()
lora.power_mode(LoRa.SLEEP)

pycom.rgbled(0x000000)
h = 0
for i in range (300000):
    h = h+1;

#WIFI

bluetooth.deinit()
wlan.deinit()
lora.power_mode(LoRa.SLEEP)

pycom.heartbeat(False)
pycom.rgbled(0x770000)
wlan.init(mode=WLAN.STA)
print('sending WLAN')
## for execute with a wifi conection, no with usb

for i in range (80):
    pycom.rgbled(0x000000)
    print('sending')
    time.sleep(0.1)
    pycom.rgbled(0x770000)
    time.sleep(0.01)

#micro
bluetooth.deinit()
wlan.deinit()
lora.power_mode(LoRa.SLEEP)

pycom.rgbled(0x000000)
h = 0
for i in range (300000):
    h = h+1;
#LORA


pycom.rgbled(0x777700)
print('sending LORA')
lora.power_mode(LoRa.ALWAYS_ON)
for i in range (250):
    s.send('Ping')
    time.sleep(0.034)

#DEEPSLEEP

machine.deepsleep(5000)
