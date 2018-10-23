import socket
import threading
import time
import binascii
import datetime
import queue
import simplejson as json
from micropyGPS import MicropyGPS
from seanav_message import SeanavMessage
from IMUMessage import IMUMessage
import config as cfg

class UDPReceiver(threading.Thread):
    def __init__(self, ip, port, queue, sensor):
        threading.Thread.__init__(self)
        self.sensor = sensor
        self.port = port
        self.ip = ip
        self.queue = queue
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.ip, self.port))
    def run(self):
        while 1:
            ## How to decide size?
            data, addr = self.s.recvfrom(256)
            if self.sensor == "IMU":
                print(data)
                message = self.read_NMEA_prop_format(data)
                json_object = json.dumps(message.__dict__)
                topic = "orientation_imu"
                queue_object = [ topic, json_object, message.__dict__ ]
                self.queue.put(queue_object)
                time.sleep(cfg.imu_freq)
            if self.sensor == "SEANAV":
                packet = self.read_NMEA_from_seanav(data)
                dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                message = SeanavMessage(dt, packet)
                json_object = json.dumps(message.__dict__)
                topic = "gps_seanav"
                queue_object = [ topic, json_object, message.__dict__ ]
                self.queue.put(queue_object)
                time.sleep(cfg.seanav_freq)
    def read_NMEA_prop_format(self, data):
        arr = data.decode('utf-8').split(',')
        
        dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        message = IMUMessage(dt, arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], arr[13], arr[14], arr[15])
        return message
    def read_NMEA_from_seanav(self, data):
        my_gps = MicropyGPS()
        for letter in data.decode():
            my_gps.update(letter)
        return my_gps

        #print("lat: " + str(my_gps.latitude))
        #print("lon: " + str(my_gps.longitude))
        #print("course: " + str(my_gps.course))
        #print("altitude: " + str(my_gps.altitude))
        #print("speed: " + str(my_gps.speed))
        #print("satellites in use: " + str(my_gps.satellites_in_use))
        #print("fix type: " + str(my_gps.fix_type))
        ## 1: no fix, 2: 2d fix, 3: 3d fix




