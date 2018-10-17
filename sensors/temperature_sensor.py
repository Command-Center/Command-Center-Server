import simplejson as json
import threading
from sense_hat import SenseHat
import queue
import datetime
import time
from temperature_message import TemperatureMessage

class TemperatureSensor(threading.Thread):
    def __init__(self, message_queue):
        threading.Thread.__init__(self)
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = True

        self.message_queue = message_queue

        
    def run(self):
        while self.sending:
            temp = round(self.sense.get_temperature(), 1)
            dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            print("temp: " + str(temp))            
            message = TemperatureMessage(dt, temp)
            
            json_object = json.dumps(message.__dict__)
            topic = "temperature"
            queue_object = [ topic, json_object ]
            self.message_queue.put(queue_object)
            time.sleep(5)
