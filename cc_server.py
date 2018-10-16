import paho.mqtt.client as mqtt
import asyncio
import threading
import time
import queue

class MQTT(threading.Thread):
    mqtt_address = "40.113.99.5"
    connected = False
    def __init__(self, message_queue):
        threading.Thread.__init__(self)
        client = mqtt.Client("some_id...")
    def run(self):
        while not self.connected:
            try:
                client.connect(self.mqtt_address)
                print("Connected")
                self.connected = True
            except Exception as e:
                self.connected = False
                print("Trying to reconnect")
            time.sleep(1)
    def subscribe(self):
        return None
    def publish(self):
        return None
    def isConnected(self):
        return self.connected
def main():
    messageQueue = queue.Queue
    print("Creating mqtt class..")
    mqtt_thread = MQTT(message_queue)
    mqtt_thread.start()
    print("Program end")
if __name__ == "__main__":
    main()
