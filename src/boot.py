def do_connect():
    import network
    from time import sleep
    from secrets import secrets
    import machine

    wlan = network.WLAN(network.STA_IF)        

    if not wlan.isconnected():                 
        print('connecting to network...')
        wlan.active(True)                     
       
        wlan.config(pm = 0xa11140)
        wlan.connect(secrets["ssid"], secrets["password"]) 
        print('Waiting for connection...', end='')
       
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            sleep(1)
 
    ip = wlan.ifconfig()[0]
    print('\nConnected on {}'.format(ip))
    return ip 



try:
    ip = do_connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

