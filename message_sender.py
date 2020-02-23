import paho.mqtt.client as mqtt
import threading
import time
import queue

class MessageSender(threading.Thread):
    sending = False
    def __init__(self, outgoing_message_queue, mqtt_connector, db_handler):
        threading.Thread.__init__(self)
        self.sending = True
        self.outgoing_message_queue = outgoing_message_queue
        self.mqtt_connector = mqtt_connector
        self.db_handler = db_handler
    def run(self):
        ## While sending and while connected
        
        while self.sending and self.mqtt_connector.connected:
            message_array = self.outgoing_message_queue.get()
            message = message_array[1]
            topic = message_array[0]
            message_dict = message_array[2]
            try:
               self.db_handler.add_to_db(message_dict, topic) 
            except Exception as e:
                print("Failed to add to db: " + str(e))
            try:
                self.mqtt_connector.publish(message, topic)
            except Exception as e:
                print("Failed to publish: " + str(e))

