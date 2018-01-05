import uwebsockets.client
import ujson as json
import uos as os

def get_cid():
    return "aa35c1d80000"

def command(uri, payload=None):
    with uwebsockets.client.connect('ws://your_tv_ip_address:3000') as websocket:
        register(websocket)
        
        json_payload = {"id":get_cid(), "type":"request"}
        
        if uri != None:
            json_payload["uri"] = uri
        if payload != None:
            json_payload["payload"] = payload
            
        json_str = json.dumps(json_payload)
        print(json_str)
        websocket.send(json_str)
        
        resp = websocket.recv()
        
        websocket.close()
    
        return resp

def register(websocket):
    f = open("pairing.json")
    pairing_payload = json.loads(f.read())
    f.close()
    
    f = open("client.key")
    client_key = f.read()
    f.close()
    
    if client_key != "":
        pairing_payload["client-key"] = client_key

    json_payload = {"id":get_cid(), "type":"register", "payload": pairing_payload}

    resp = None
    websocket.send(json.dumps(json_payload))
    while True:
        fin, opcode, data = websocket.read_frame()
        resp = json.loads(data)
        if(resp["type"] == "registered"):
            break
    
    if client_key == "":
        f = open("client.key", 'w')
        f.write(resp["payload"]["client-key"])
        f.close()
