import time  # Allows use of time.sleep() for delays
from mqtt import MQTTClient  # For use of MQTT protocol to talk to Adafruit IO
import ubinascii  # Conversions between binary data and various encodings
import machine  # Interfaces with hardware components
import micropython  # Needed to run any MicroPython code
import random  # Random number generator
from machine import Pin  # Define pin
import network




from tempsensor import get_temp_humidity
from lightsensor import check_light
from magnetdetected import is_magnet_detected

# BEGIN SETTINGS

led = Pin("LED", Pin.OUT)  # led pin initialization for Raspberry Pi Pico W

# Wireless network


WIFI_SSID = "Tele2_763d45"
WIFI_PASS = "dtm2nxum"  # No this is not our regular password. :)

# Adafruit IO (AIO) configuration

AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "noorMustafa"
AIO_KEY = "aio_zXiQ3552PEbFzlTycPnyp2Ek3gDV"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_LIGHTS_FEED = "noorMustafa/feeds/lighting"
AIO_TEMP_FEED = "noorMustafa/feeds/temperature"
AIO_DOOR_FEED = "noorMustafa/feeds/door"

# END SETTINGS


# FUNCTIONS














# Function to connect Pico to the WiFi
def do_connect():

    
    import network
    from time import sleep
    import machine

    wlan = network.WLAN(network.STA_IF)  # Put modem on Station mode

    if not wlan.isconnected():  # Check if already connected
        print("connecting to network...")
        wlan.active(True)  # Activate network interface
        # set power mode to get WiFi power-saving off (if needed)
        wlan.config(pm=0xA11140)
        wlan.connect(WIFI_SSID, WIFI_PASS)  # Your WiFi Credential
        print("Waiting for connection...", end="")
        # Check if it is connected otherwise wait
        while not wlan.isconnected() and wlan.status() >= 0:
            print(".", end="")
            sleep(1)
    # Print the IP assigned by router
    ip = wlan.ifconfig()[0]
    print("\nConnected on {}".format(ip))
    return ip



# temp, hum = get_temp_humidity()
# print(temp)





def send_tempsensor_data():

    temp, hum = get_temp_humidity()
    
    try:
        client.publish(topic=AIO_TEMP_FEED, msg=str(temp))
        print("DONE")
        print(temp)
    except Exception as e:
        print("FAILED")





















# Callback Function to respond to messages from Adafruit IO
def sub_cb(topic, msg):  # sub_cb means "callback subroutine"
    print((topic, msg))  # Outputs the message that was received. Debugging use.
    if msg == b"ON":  # If message says "ON" ...
        led.on()  # ... then LED on
    elif msg == b"OFF":  # If message says "OFF" ...
        led.off()  # ... then LED off
    else:  # If any other message is received ...
        print("Unknown message")  # ... do nothing but output that it happened.






# Try WiFi Connection
try:
    ip = do_connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

# Use the MQTT protocol to connect to Adafruit IO
client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)

# Subscribed messages will be delivered to this callback
client.set_callback(sub_cb)
client.connect()
client.subscribe(AIO_LIGHTS_FEED)
print("Connected to %s, subscribed to %s topic" % (AIO_SERVER, AIO_LIGHTS_FEED))


try:  # Code between try: and finally: may cause an error
    # so ensure the client disconnects the server if
    # that happens.
    while 1:  # Repeat this loop forever
        client.check_msg()  # Action a message if one is received. Non-blocking.
 
        send_tempsensor_data()
        print(check_light())
        client.publish(topic=AIO_LIGHTS_FEED , msg=str(check_light()))
        client.publish(topic=AIO_DOOR_FEED , msg=str(is_magnet_detected()))
        print(is_magnet_detected())
        


    



        time.sleep(8)
finally:  # If an exception is thrown ...
    client.disconnect()  # ... disconnect the client and clean up.
    client = None
    print("Disconnected from Adafruit IO.")
