import simplejson as json
import threading
import queue
import datetime
from sense_hat import SenseHat
from temperature_message import TemperatureMessage

class AccelerationSensor(threading.Thread):
    def __init__(self, message_queue):
        threading.Thread.__init__(self)
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = True

        self.message_queue = message_queue

        self.run()
    def run(self):
        while sending:
            acceleration = self.sense.get_accelerometer_raw()
            x = str(round(acceleration['x'], 2))
            y = str(round(acceleration['y'], 2))
            z = str(round(acceleration['z'], 2))

            dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            
            message = {"timestamp" : dt, "x" : x, "y" : y, "z" : z}
            
            json_object = json.dump(message.__dict__)
            self.message_queue.put(json_object)
            time.sleep(1)