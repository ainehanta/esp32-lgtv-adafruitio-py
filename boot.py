
SSID_NAME = "D80F99D2FEF4-2G"
SSID_PASS = "2215000452211"

import utime
import network

def connect_wifi(ssid, passkey, timeout=10):
    wifi= network.WLAN(network.STA_IF)
    if wifi.isconnected() :
        print('already Connected.    connect skip')
        return wifi
    else :
        wifi.active(True)
        wifi.connect(ssid, passkey)
        while not wifi.isconnected() and timeout > 0:
            print('.')
            utime.sleep(1)
            timeout -= 1

    if wifi.isconnected():
        print('Connected')
        return wifi
    else:
        print('Connection failed!')
        return null

if __name__ == "__main__":
    wifi = connect_wifi(SSID_NAME, SSID_PASS)
    if not wifi :
        sys.exit(0)
