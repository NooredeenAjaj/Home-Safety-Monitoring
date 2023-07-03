import time  
from mqtt import MQTTClient  
import ubinascii  
import machine  
import micropython  
import random  
from machine import Pin  
import network
from boot import  connect




from tempsensor import get_temp
from lightsensor import check_light
from magnetdetected import is_magnet_detected


led = Pin("LED", Pin.OUT)  






AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "yourname"
AIO_KEY = "ad"

AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  
AIO_LIGHTS_FEED = "noorMustafa/feeds/lighting"
AIO_TEMP_FEED = "noorMustafa/feeds/temperature"
AIO_DOOR_FEED = "noorMustafa/feeds/door"












def sub_cb(topic, msg): 
    print((topic, msg))  
    if msg == b"ON": 
        led.on()  
    elif msg == b"OFF": 
        led.off() 
    else:  
        print("Unknown message")  






# Try WiFi Connection
try:
    ip = connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

# Use the MQTT protocol to connect to Adafruit IO
client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)

# Subscribed messages will be delivered to this callback
client.set_callback(sub_cb)
client.connect()
client.subscribe(AIO_LIGHTS_FEED)
print("Connected to %s, subscribed to %s topic" % (AIO_SERVER, AIO_LIGHTS_FEED))


try: 
    while 1:  
        client.check_msg() 
 
        client.publish(topic=AIO_TEMP_FEED, msg=str(get_temp()))
        client.publish(topic=AIO_LIGHTS_FEED , msg=str(check_light()))
        client.publish(topic=AIO_DOOR_FEED , msg=str(is_magnet_detected()))

        


    



        time.sleep(8)
finally: 
    client.disconnect()
    client = None
    print("Disconnected from Adafruit IO.")
