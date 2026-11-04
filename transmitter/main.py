# Import config
from lib.config import Config

from machine import Pin
import machine
import network
import urequests
import json
import utime


def do_connect(wlan: network.WLAN):
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(Config.NETWORK_CONFIG["SSID"], Config.NETWORK_CONFIG["PASSWORD"])
        while not wlan.isconnected():
            machine.idle()
    print('network config:', wlan.ipconfig('addr4'))

def toggle_switch():
    try: 
        response = urequests.get(f"http://192.168.4.1/toggle")
        utime.sleep(1)
        print(response.text)
        response.close()
    except Exception as e:
        print(repr(e))

def main():

    button = Pin(Config.BUTTON_CONFIG["BUTTON_PORT"], Pin.IN, Pin.PULL_UP)
    wlan = network.WLAN(network.STA_IF)

    do_connect(wlan)

    while True:
        if (wlan.isconnected()):
            if button.value() == 0:  
                utime.sleep_ms(20)
            
            if button.value() == 0:
                toggle_switch()
                
                while button.value() == 0:
                    utime.sleep_ms(10)
        else:
            print("Not connected to network, attempting to connect")
            do_connect(wlan)
            utime.sleep(0.5)


if __name__ == "__main__":
    main()
