import time
import os
import ujson as json

import machine
from umqtt.simple import MQTTClient
import wol
import lgtv

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('your_wifi_ssid', 'your_wifi_pass')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
        
def sub_cb(topic, msg):
    print((topic, msg))
    action = json.loads(msg)
    if action['type'] == 'wol':
        for i in range(5):
            # change to your tv's mac address
            wol.send(b'\xAA\xBB\xCC\xDD\xEE\xFF')
            time.sleep(1)
    elif action['type'] == 'off':
        lgtv.command("ssap://system/turnOff")
    elif action['type'] == 'volume-up':
        lgtv.command("ssap://audio/volumeUp")
    elif action['type'] == 'volume-down':
        lgtv.command("ssap://audio/volumeDown")

def main():
    c = MQTTClient("your_aio_name", "io.adafruit.com", user="your_aio_name", password="your_aio_active_key", ssl=True)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(b"your_aio_name/feeds/lgtv-action")
    
    def check_msg():
        try:
            c.check_msg()
        except OSError:
            print("ENOENT")
            machine.reset()
    
    epoch = 0
    prev_epoch = 0
    while True:
        epoch = time.time()
        if epoch != prev_epoch:
            if epoch % 5 == 0:
                check_msg()
        prev_epoch = epoch

if __name__ == "__main__":
    do_connect()
    main()
