import network
#ssid = "D31-lab"
#key = "IoT.SPSE.lab22"

ssid = "Raspberry"
key = "rpipico123"

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig())

do_connect()