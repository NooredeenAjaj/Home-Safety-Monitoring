
import dht
from machine import ADC, Pin
import time
import math
from math import log

BETA = 3950
KELVIN_CONSTANT = 273.15

def get_temp():

    thermistor_pin = ADC(28)

    try:
        RawADC = thermistor_pin.read_u16()
        Temp = math.log(((10240000 / RawADC) - 10000))
        Temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * Temp * Temp ))* Temp)
        Temp = Temp - 273.15  # Convert Kelvin to Celsius
       




        return round(Temp) 
    except Exception as error:
        print("Exception occurred", error)
        return None
    





