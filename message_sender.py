import paho.mqtt.client as mqtt
import threading
import time
import queue

class MessageSender(threading.Thread):
    sending = False
    def __init__(self, outgoing_message_queue, mqtt_connector):
        ## something
        threading.Thread.__init__(self)
        self.sending = True
        self.outgoing_message_queue = outgoing_message_queue
        self.mqtt_connector = mqtt_connector
    def run(self):
        ## While sending and while connected
        print("Attempting to start runner")
        
        while self.sending and self.mqtt_connector.connected:
            message_array = self.outgoing_message_queue.get()
            message = message_array[1]
            topic = message_array[0]
            try:
                self.mqtt_connector.publish(message, topic)
            except Exception as e:
                print("Failed to publish: " + str(e))
                

    