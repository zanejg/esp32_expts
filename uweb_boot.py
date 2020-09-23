# Complete project details at https://RandomNerdTutorials.com

try:
    import usocket as socket
except:
    import socket

from machine import Pin
import network
import time
import sys
import uos
import esp
esp.osdebug(None)

import gc

import settings

gc.collect()

ssid = settings.ssid
password = settings.password

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)
