from machine import ADC, Pin

def check_light():
   
    ldr = ADC(Pin(27))
    led = Pin("LED", Pin.OUT)

    light = ldr.read_u16()
    darkness = round(light / 65535 * 10000, 2)
    if darkness >= 70:

        led.on()
        return "w:night-clear"
    else:

        led.off()
        return "w:day-sunny"
