import paho.mqtt.client as mqtt
import asyncio
import threading
import time

class MQTT(threading.Thread):
    mqtt_address = "40.113.99.5"
    connected = False
    def __init__(self):
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
def main():
    print("Creating mqtt class..")
    mqtt_thread = MQTT()
    mqtt_thread.start()
    print("Program end")
if __name__ == "__main__":
    main()
