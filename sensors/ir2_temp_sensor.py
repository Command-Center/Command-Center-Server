import simplejson as json
import threading
import queue
import datetime
import minimalmodbus
from temperature_message import TemperatureMessage

class IR2TemperatureSensor(threading.Thread):
    def __init__(self, message_queue):
        threading.Thread.__init__(self)
        self.instrument = minimalmodbus.Instrument('/dev/ttyUSB-IR1', 1)
        self.instrument.serial.baudrate = 9600
        self.sending = True

        self.message_queue = message_queue

        self.run()
    def run(self):
        while sending:
            self.instrument = minimalmodbus.Instrument('/dev/ttyUSB-IR2', 1)
            self.instrument.serial.baudrate = 9600
            temp = round(self.instrument.read_register(16, 1), 1)
            dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            
            message = TemperatureMessage(dt, temp)
            
            json_object = json.dump(message.__dict__)
            self.message_queue.put(json_object)
            time.sleep(5)