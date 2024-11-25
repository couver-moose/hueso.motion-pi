from machine import Pin
from time import sleep
import network
import urequests  # Verwendung von urequests anstelle von requests
import json, gc

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
led = Pin(16, Pin.OUT)
button = Pin(15, Pin.IN, Pin.PULL_DOWN)

#configure wifi
ssid = 'FRITZ!Box 6660 Cable AC'
password = '39578827442446628775'

#configure bridge connection
bridge = "192.168.178.21"
auth = "HJmaGj86m7iUN0TSgKyzUo9TU4Eg8nFctr9bwiFI"

#configure light
light = 3

#setup url interfaces
url = f"https://{bridge}/api/{auth}/lights/{light}/state"


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
urequests.request("PUT", url, data=off)
gc.collect()

light = False

#main loop
while True:
    try:
        if button.value():
            led.toggle()
            light = not light
            if light:
                print("turn light on")
                urequests.request("PUT", url, data=on)
                gc.collect()        
            else:
                print("turn light off")
                urequests.request("PUT", url, data=off)
                gc.collect()
    except KeyboardInterrupt:
        machine.reset()
    sleep(0.05)