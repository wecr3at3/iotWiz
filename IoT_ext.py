import ubinascii
import machine
import micropython
import _thread as th
import time
from umqttsimple import MQTTClient
from machine import Pin

# Initialize output pins
sw1 = Pin(15, Pin.OUT, value = 1)
sw2 = Pin(2, Pin.OUT, value = 1)
sw3 = Pin(4, Pin.OUT, value = 1)
sw4 = Pin(5, Pin.OUT, value = 1)

# Set the keepalive time (interval between pings to the MQTT broker)
alive_time = 30

# Set up MQTT connection
SERVER = "io.adafruit.com"
CLIENT_ID = "iot3xt"
TOPIC1 = b"icreate/feeds/wecreate.relay1"
TOPIC2 = b"icreate/feeds/wecreate.relay2"
TOPIC3 = b"icreate/feeds/wecreate.relay3"
TOPIC4 = b"icreate/feeds/wecreate.relay4"

# Callback function to be executed when a message is received from the MQTT broker
def sub_cb(topic, msg):
    # Update the output pins based on the received message
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

# Function to continuously ping the MQTT broker
def ping_wait(client):
    while True:
        # Sleep for the keepalive time
        for i in range(alive_time):
            machine.idle()
        # Ping the broker
        client.ping()
        print("Pinging...")

# Connect to the MQTT broker and set up subscriptions
def main(server=SERVER):
    # Create MQTT client
    client = MQTTClient(CLIENT_ID, server, user = 'icreate', password = '74733f4f39b54bf1b49a04f71f2769f1', keepalive = alive_time)
    # Set the callback function
    client.set_callback(sub_cb)
    # Connect to the broker
    client.connect()
    # Subscribe to topics
    client.subscribe(TOPIC1)
    client.subscribe(TOPIC2)
    client.subscribe(TOPIC3)
    client.subscribe(TOPIC4)
    # Retain the last published value by MQTT broker
    client.publish(b"icreate/feeds/wecreate.relay1/get", b"hello")
    client.publish(b"icreate/feeds/wecreate.relay2/get", b"hello")
    client.publish(b"icreate/feeds/wecreate.relay3/get", b"hello")
    client.publish(b"icreate/feeds/wecreate.relay4/get", b"hello")
    print("Connected to %s, subscribed to %s, %s, %s and %s topics" % (server, TOPIC1, TOPIC2, TOPIC3, TOPIC4))

    # Start a thread to ping the broker
    th.start_new_thread(ping_wait, (client,))
    
    try:
        while True:
            client.wait_msg()

    except OSError as e:
        print("Reconnecting...")
        machine.reset()

    finally:
        client.disconnect()

try:
    main()

except OSError as e:
    print("Failed to connect to MQTT broker. Reconnecting...")
    main()
