import threading
import time
from sense_hat import SenseHat

class PressureSensor(threading.Thread):
    def __init__(self, message_queue):
        threading.Thread.__init__(self)
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = False
        self.message_queue = message_queue
    def run():
        while self.sending:
            pressure = round(self.sense.get_pressure(), 1)
            dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        
        ## Consider changing name from temp to more general.
        ## We'll see what is needed.
        ## Might be able to use the same class for everything.
        

            message = TemperatureMessage(dt, pressure)
        
            json_object = json.dumps(message.__dict__)
            topic = "pressure"
            queue_object = [ topic, json_object ]
            self.message_queue.put(queue_object)
            time.sleep(5)
