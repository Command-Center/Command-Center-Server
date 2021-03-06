import simplejson as json
import threading
import queue
import datetime
import time
import gpsd
import subprocess
from temperature_message import TemperatureMessage
import config as cfg

class GpsSensor(threading.Thread):
    def __init__(self, message_queue):
        threading.Thread.__init__(self)
        setup_gps()
        self.sending = True

        self.message_queue = message_queue
        

        
    def run(self):
        while self.sending:
            try:
                packet = gpsd.get_current()
                
                dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            
                message = GpsMessage(dt, packet)
            
                json_object = json.dumps(message.__dict__)
                topic = "gps"
                queue_object = [ topic, json_object ]
                self.message_queue.put(queue_object)
                
                first_fix = True
            except Exception as e:
                print("GPS FEIL: " + str(e))
            
            ## Can have different freqs for connected/not_connected

            if first_fix:
                time.sleep(cfg.gps_freq)
            else:
                time.sleep(cfg.gps_freq_if_no_fix)
    def setup_gps():
        killall = "sudo killall gpsd"
        stop = "sudo systemctl stop gpsd.socket"
        disable = "sudo systemctl disable gpsd.socket"
        start = "sudo gpsd /dev/ttyUSB-GPS -F /var/run/gpsd.sock"
        c = killall + "; " + stop + "; " + disable + "; " + start
        process = subprocess.Popen(c, stdout=subprocess.PIPE, shell=True)
        proc = process.communicate()

        gpsd.connect()
