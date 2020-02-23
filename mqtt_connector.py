
import paho.mqtt.client as mqtt
import threading
import time
import queue
import config as cfg

class MqttConnector(threading.Thread):
    mqtt_address = cfg.ip_mqtt ##Frost server
    
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
            time.sleep(cfg.reconnect_interval_mqtt)
        
    def subscribe(self):
        return None
    def publish(self, message, topic):
        self.client.publish(topic, message)
    def isConnected(self):
        return self.connected
