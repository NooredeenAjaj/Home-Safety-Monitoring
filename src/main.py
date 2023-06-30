import time 
from mqtt import MQTTClient  
import ubinascii  
import machine  
import micropython  
import random  
from machine import Pin 
import network




from tempsensor import get_temp_humidity
from lightsensor import check_light
from magnetdetected import is_magnet_detected



led = Pin("LED", Pin.OUT)  



WIFI_SSID = "Tele2_763d45"
WIFI_PASS = "dtm2nxum"  



AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "noorMustafa"
AIO_KEY = "aio_zXiQ3552PEbFzlTycPnyp2Ek3gDV"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  
AIO_LIGHTS_FEED = "noorMustafa/feeds/lighting"
AIO_TEMP_FEED = "noorMustafa/feeds/temperature"
AIO_DOOR_FEED = "noorMustafa/feeds/door"















# Function to connect Pico to the WiFi
def do_connect():

    
    import network
    from time import sleep
    import machine

    wlan = network.WLAN(network.STA_IF)  

    if not wlan.isconnected():  
        print("connecting to network...")
        wlan.active(True)  
       
        wlan.config(pm=0xA11140)
        wlan.connect(WIFI_SSID, WIFI_PASS) 
        print("Waiting for connection...", end="")
       
        while not wlan.isconnected() and wlan.status() >= 0:
            print(".", end="")
            sleep(1)

    ip = wlan.ifconfig()[0]
    print("\nConnected on {}".format(ip))
    return ip









def send_tempsensor_data():

    temp, hum = get_temp_humidity()
    
    try:
        client.publish(topic=AIO_TEMP_FEED, msg=str(temp))
        print("DONE")
        print(temp)
    except Exception as e:
        print("FAILED")






















def sub_cb(topic, msg):  
    print((topic, msg)) 
    if msg == b"ON":  
        led.on()  
    elif msg == b"OFF": 
        led.off() 
    else:  
        print("Unknown message") 







try:
    ip = do_connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")


client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)


client.set_callback(sub_cb)
client.connect()
client.subscribe(AIO_LIGHTS_FEED)
print("Connected to %s, subscribed to %s topic" % (AIO_SERVER, AIO_LIGHTS_FEED))


try:  

    while 1:  
        client.check_msg()  
 
        send_tempsensor_data()
        print(check_light())
        client.publish(topic=AIO_LIGHTS_FEED , msg=str(check_light()))
        client.publish(topic=AIO_DOOR_FEED , msg=str(is_magnet_detected()))
        print(is_magnet_detected())
        


    



        time.sleep(8)
finally: 
    client.disconnect()  
    client = None
    print("Disconnected from Adafruit IO.")
