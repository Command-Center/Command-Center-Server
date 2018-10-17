import simplejson as json
import threading
import queue
import datetime
import gpsd
import subprocess
from temperature_message import TemperatureMessage

class GpsSensor(threading.Thread):
    def __init__(self, message_queue):
        threading.Thread.__init__(self)
        setup_gps()
        self.sending = True

        self.message_queue = message_queue
        

        self.run()
    def run(self):
        while self.sending:
            try:
                packet = gpsd.get_current()
                
                dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            
                message = GpsMessage(dt, packet)
            
                json_object = json.dump(message.__dict__)
                self.message_queue.put(json_object)
                
                first_fix = True
            except Exception as e:
                print("GPS FEIL: " + str(e))
            
            ## Can have different freqs for connected/not_connected

            if first_fix:
                time.sleep(1)
            else:
                time.sleep(1)
    def setup_gps():
        killall = "sudo killall gpsd"
        stop = "sudo systemctl stop gpsd.socket"
        disable = "sudo systemctl disable gpsd.socket"
        start = "sudo gpsd /dev/ttyUSB-GPS -F /var/run/gpsd.sock"
        c = killall + "; " + stop + "; " + disable + "; " + start
        process = subprocess.Popen(c, stdout=subprocess.PIPE, shell=True)
        proc = process.communicate()

        gpsd.connect()