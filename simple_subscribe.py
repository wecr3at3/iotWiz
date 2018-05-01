import machine,time
from machine import Pin
from umqtt.simple import MQTTClient

ledPin = 2
Pin(ledPin,Pin.OUT,value = 1)

state = 0

def sub_cb(ledTopic, msg):
    global state
    print((ledTopic, msg))
    if msg == b"on":
	print('Recieved:',msg)
        led.value(0)
        state = 1
    elif msg == b"off":
	print('Recieved:',msg)
        led.value(1)
        state = 0
    elif msg == b"toggle":
        # LED is inversed, so setting it to current state
        # value will make it toggle
        led.value(state)
        state = 1 - state
    else:
        print('I didn\'t recieve shit!')

myEspClient = MQTT("15c64500-4965-11e8-b4ef-898f2f5b9050","mqtt.mydevices.com",1883,"2689f050-995a-11e7-b0e9-e9adcff3788e","c320eee89ad304367312c68a8a0b5d05ac0f385e")
myEspClient.set_callback(sub_cb)
myEspClient.connect()
#
# subscribing to a TOPIC at cayenne. Atleast 1 argument required
#
myEspClient.subscribe(b"v1/2689f050-995a-11e7-b0e9-e9adcff3788e/things/15c64500-4965-11e8-b4ef-898f2f5b9050/data/0")
time.sleep(500)

try:
	myEspClient.wait_msg()
finally:
	myEspClient.disconnect()
	print('Connection Lost with the Broker')






