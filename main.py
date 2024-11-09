from gpiozero import *
import time

bridge = "192.168.178.21"
auth = "gi3EDZaV8eCaB159ZWsDeHaxPRhB4Dr8CCGpmR6O"

response = requests.get(f"https://{bridge}/api/{auth}/lights", verify=False)

light1on = {
    'which':4,
    'data':{
        'state':{'on':True}
    }
}

light2on = {
    'which':5,
    'data':{
        'state':{'on':True}
    }
}

light1off= {
    'which':4,
    'data':{
        'state':{'on':False}
    }
}

light2off= {
    'which':5,
    'data':{
        'state':{'on':False}
    }
}

bridge.light.update(resource)

led = LED(17)
pir = MotionSensor(24)

while True:
    pir.wait_for_motion()
    led.on()
    bridge.light.update(light1on)
    bridge.light.update(light2on)
    print("You moved")
    pir.wait_for_no_motion()
    led.off()
    bridge.light.update(light1off)
    bridge.light.update(light2off)
    print("Dario ist ein Hurensogn")