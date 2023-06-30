from machine import Pin

# Pin setup
digitalPin = Pin(16, Pin.IN)

def is_magnet_detected():
    digitalValue = digitalPin.value()
   
    if digitalValue == True:
       return"Alert! Door has been opened."

    else:
        return "Status: All secure." 
