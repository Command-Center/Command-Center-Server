import simplejson as json
import threading
from sense_hat import SenseHat
import queue
import datetime
from temperature_message import TemperatureMessage

class TemperatureSensor(threading.Thread):
    def __init__(self, message_queue):
        threading.Thread.__init__(self)
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = True

        self.message_queue = message_queue

        self.run()
    def run(self):
        while sending:
            temp = round(self.sense.get_temperature(), 1)
            dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            
            message = TemperatureMessage(dt, temp)
            
            json_object = json.dump(message.__dict__)
            self.message_queue.put(json_object)
            time.sleep(5)