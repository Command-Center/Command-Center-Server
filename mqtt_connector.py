
import paho.mqtt.client as mqtt
import threading
import time
import queue

class MqttConnector(threading.Thread):
    mqtt_address = "40.113.99.5" ##Frost server
    
    connected = False
    def __init__(self):
        threading.Thread.__init__(self)
        self.client = mqtt.Client("some_id...")
    def run(self):
        while not self.connected:
            try:
                self.client.connect(self.mqtt_address)
                print("Connected")
                self.connected = True
            except Exception as e:
                self.connected = False
                print("Trying to reconnect")
                print(e)
            time.sleep(1)
        
    def subscribe(self):
        return None
    def publish(self, message):
        self.client.publish("test", message)
    def isConnected(self):
        return self.connected
