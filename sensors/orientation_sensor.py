import simplejson as json
import threading
import queue
import datetime
# from sense_hat import SenseHat
from temperature_message import TemperatureMessage

class OrientationSensor(threading.Thread):
    def __init__(self, message_queue):
        threading.Thread.__init__(self)
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = True

        self.message_queue = message_queue

        self.run()
    def run(self):
        while sending:
            orientation = self.sense.get_orientation()
            pitch = str(round(orientation["pitch"], 2))
            roll = str(round(orientation["roll"], 2))
            yaw = str(round(orientation["yaw"], 2))
            
            dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            
            message = {"timestamp" : dt, "pitch" : pitch, "roll" : roll, "yaw" : yaw}
            
            json_object = json.dump(message.__dict__)
            self.message_queue.put(json_object)
            time.sleep(1)