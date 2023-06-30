from machine import ADC, Pin

def check_light():
   
    ldr = ADC(Pin(27))


    light = ldr.read_u16()
    darkness = round(light / 65535 * 10000, 2)
    if darkness >= 70:


        return "w:night-clear"
    else:


        return "w:day-sunny"
