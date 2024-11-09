from gpiozero import *
import time
import requests
import json

bridge = "192.168.178.21"
auth = "HJmaGj86m7iUN0TSgKyzUo9TU4Eg8nFctr9bwiFI"
light_4 = 4
light_5 = 5
url_1 = f"https://{bridge}/api/{auth}/lights/{light_4}/state"
url_2 = f"https://{bridge}/api/{auth}/lights/{light_5}/state"
print(url_1)
print(url_2)

on = json.dumps({
"on": True, "sat":254, "bri":254,"hue":283 
})

off = json.dumps({
"on": False
})

led = LED(17)
pir = MotionSensor(24)

while True:
    pir.wait_for_motion()
    led.on()
    requests.request("PUT", url_1, data=on, verify=False)
    print("an")
    time.sleep(0.5)
    print("aus")
    led.off()
    requests.request("PUT", url_1, data=off, verify=False)
    time.sleep(0.5)
    led.on()
    requests.request("PUT", url_1, data=on, verify=False)
    requests.request("PUT", url_2, data=on, verify=False)
    print("Bewegung erkannt")
    
    pir.wait_for_no_motion()
    time.sleep(10)
    led.off() #hallo bekka!was geht ab? hiiier!!! HAllloo
    requests.request("PUT", url_1, data=off, verify=False)
    requests.request("PUT", url_2, data=off, verify=False)
    print("Keine Bewegung mehr")