import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes 
import threading
import time
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("lorris_plants/regar/response", 2),("lorris_plants/photo/response", 2)]) 
# The callback for when a PUBLISH message is received from the server.

    
client = mqtt.Client(client_id="bot-lorris")

def  connect(on_message):
    global client 
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.0.224", 1883, 60)

    x = threading.Thread(target=client.loop_forever)
    x.start()    
    
    
def regar():
    
    properties=Properties(PacketTypes.PUBLISH)
    properties.MessageExpiryInterval=20 # in seconds
    print("publicando en regar")
    client.publish("lorris_plants/request","regar",1,properties=properties)

def photo():
    
    properties=Properties(PacketTypes.PUBLISH)
    properties.MessageExpiryInterval=20 # in seconds
    print("publicando en photo")
    client.publish("lorris_plants/request","photo",1,properties=properties)
  
 
 
    
def on_message(client, userdata, msg):
    print(msg.topic+" - "+str(msg.payload))

if __name__ =="__main__":
    print("conectando")
    connect(on_message)
    print("conectado")
    #publish("hola cotorra")
    time.sleep(5)