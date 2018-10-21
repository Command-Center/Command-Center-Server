import threading
import time
import datetime
import simplejson as json
from sense_hat import SenseHat
from temperature_message import TemperatureMessage
import config as cfg

class HumiditySensor(threading.Thread):
    def __init__(self, message_queue):
        threading.Thread.__init__(self)
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = True
        self.message_queue = message_queue
    def run(self):
        while self.sending:
            humidity = round(self.sense.get_humidity(), 1)
            dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        
        ## Consider changing name from temp to more general.
        ## We'll see what is needed.
        ## Might be able to use the same class for everything.
        

            message = TemperatureMessage(dt, float(humidity))
        
            json_object = json.dumps(message.__dict__)
            topic = "humidity"
            queue_object = [ topic, json_object, message.__dict__ ]
            self.message_queue.put(queue_object)
            time.sleep(cfg.humidity_freq)
