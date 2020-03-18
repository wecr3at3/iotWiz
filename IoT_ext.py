from umqttsimple import MQTTClient
from machine import Pin
import ubinascii
import machine
import micropython
import _thread as th 
import time

sw1 = Pin(15, Pin.OUT, value = 1)
sw2 = Pin(2, Pin.OUT, value = 1)
sw3 = Pin(4, Pin.OUT, value = 1)
sw4 = Pin(5, Pin.OUT, value = 1)

pingLed = Pin(4, Pin.OUT)

# keep the connection between MQTT broker and client open for a specified time
alive_time = 30

SERVER = "io.adafruit.com"
CLIENT_ID = "iot3xt"

# subscribe to the following feeds
TOPIC1 = b"icreate/feeds/wecreate.relay1"
TOPIC2 = b"icreate/feeds/wecreate.relay2"
TOPIC3 = b"icreate/feeds/wecreate.relay3"
TOPIC4 = b"icreate/feeds/wecreate.relay4"

# do this when received a message from the MQTT broker
def sub_cb(topic, msg):
    print((topic, msg))
    if msg == b"ON" and topic == TOPIC1:
        sw1.value(0)
    elif msg == b"OFF" and topic == TOPIC1:
        sw1.value(1)
    elif msg == b"ON" and topic == TOPIC2:
        sw2.value(0)
    elif msg == b"OFF" and topic == TOPIC2:
        sw2.value(1)
    elif msg == b"ON" and topic == TOPIC3:
        sw3.value(0)
    elif msg == b"OFF" and topic == TOPIC3:
        sw3.value(1)
    elif msg == b"ON" and topic == TOPIC4:
        sw4.value(0)
    elif msg == b"OFF" and topic == TOPIC4:
        sw4.value(1)


def main(server=SERVER):
    c = MQTTClient(CLIENT_ID, server, user = 'icreate', password = '74733f4f39b54bf1b49a04f71f2769f1', keepalive = alive_time)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC1)
    c.subscribe(TOPIC2)
    c.subscribe(TOPIC3)
    c.subscribe(TOPIC4)
    # retain the last published value by MQTT broker
    c.publish(b"icreate/feeds/wecreate.relay1/get", b"hello")
    c.publish(b"icreate/feeds/wecreate.relay2/get", b"hello")
    c.publish(b"icreate/feeds/wecreate.relay3/get", b"hello")
    c.publish(b"icreate/feeds/wecreate.relay4/get", b"hello")
    print("Connected to %s, subscribed to %s, %s, %s and %s topics" % (server, TOPIC1, TOPIC2, TOPIC3, TOPIC4))

    # function to continuously ping the MQTT broker in order to keep the connection alive
    def ping_wait():
        while True:
            for i in range(alive_time):
                time.sleep(1)
            c.ping()
            print("Pinging...")
            #for i in range(4):
                #pingLed.value(not pingLed.value())
                #time.sleep(0.1)

    # start a thread to ping the broker        
    th.start_new_thread(ping_wait,())
    
    try:
        while True:
            c.wait_msg()

    except OSError as e:
        print("Reconnecting...")
        machine.reset()

    finally:
        c.disconnect()

try:
	main()

except OSError as e:
	print("Host unreachable, Reconnecting...")
	machine.reset()


