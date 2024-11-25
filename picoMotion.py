from machine import Pin
from time import sleep
import network
import urequests  # Verwendung von urequests anstelle von requests
import json
import gc

#build connection
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


# configure pins
led = Pin(18, Pin.OUT)
motion_sensor = Pin(15, Pin.IN)

#configure wifi
ssid = 'FRITZ!Box 6660 Cable AC'
password = '39578827442446628775'

#configure bridge connection
bridge = "192.168.178.21"
auth = "HJmaGj86m7iUN0TSgKyzUo9TU4Eg8nFctr9bwiFI"

#configure lights
light_4 = 4
light_5 = 5

#setup url interfaces
url_1 = f"https://{bridge}/api/{auth}/lights/{light_4}/state"
url_2 = f"https://{bridge}/api/{auth}/lights/{light_5}/state"

#trying to connect
try:
    ip = connect()
except KeyboardInterrupt:
    machine.reset()
    
on = json.dumps({
"on": True, "sat":254, "bri":254,"hue":283 
})

off = json.dumps({
"on": False
})

#initial off
led.value(0)
urequests.request("PUT", url_1, data=off)
urequests.request("PUT", url_2, data=off)
gc.collect()

#main loop
while True:
    try:
        if motion_sensor.value():
            led.value(1)
            urequests.request("PUT", url_1, data=on)
            urequests.request("PUT", url_2, data=on)
            gc.collect()
            print("Bewegung erkannt! Lampe an.")
            sleep(10)
            led.value(0)
            urequests.request("PUT", url_1, data=off)
            urequests.request("PUT", url_2, data=off)
            gc.collect()
        else:
            print("Keine Bewegung. Lampe aus.")
    except KeyboardInterrupt:
        machine.reset()
    sleep(0.05)
