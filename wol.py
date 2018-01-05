
import usocket as socket

def send(mac, ipaddr="255.255.255.255", port=9):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    p = b'\xff' * 6 + mac * 16
    s.sendto(p, (ipaddr, port))
    
    s.close()
