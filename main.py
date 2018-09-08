import time
import os
import ujson as json

import machine
from umqtt.simple import MQTTClient
import wol
import lgtv
import IRaeha

ir_tx = IRaeha.Transmitter(pin=25)

def sub_cb(topic, msg):
    print((topic, msg))
    action = json.loads(msg)
    if action['type'] == 'wol':
        for i in range(5):
            # change to your tv's mac address
            wol.send(b'\xC8\x08\xE9\xAB\x40\x91')
            time.sleep(1)
    elif action['type'] == 'off':
        lgtv.command("ssap://system/turnOff")
    elif action['type'] == 'volume-up':
        lgtv.command("ssap://audio/volumeUp")
    elif action['type'] == 'volume-down':
        lgtv.command("ssap://audio/volumeDown")
    elif action['type'] == 'ceiling-sw':
        for i in range(4):
            ir_tx.send([0x34, 0x4A, 0x90, 0x0C, 0x9C])
            time.sleep(1)

def main():
    c = MQTTClient("ainehanta", "io.adafruit.com", user="ainehanta", password="", ssl=True)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(b"ainehanta/feeds/lgtv-action")

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
            if epoch % 1 == 0:
                check_msg()
        prev_epoch = epoch

if __name__ == "__main__":
    main()
