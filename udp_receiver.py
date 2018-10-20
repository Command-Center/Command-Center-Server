import socket
import threading
import time
import binascii
import datetime
import queue
import simplejson as json
from micropyGPS import MicropyGPS

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
            data, addr = self.s.recvfrom(100)
            if self.sensor == "IMU":
                res = self.read_NMEA_prop_format(data)
                dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                message = {"timestamp": dt, "pitch" : res[1], "roll" : res[0]}
                json_object = json.dumps(message)
                topic = "orientation_imu"
                queue_object = [ topic, json_object, message ]
                self.queue.put(queue_object)
                time.sleep(0.3)
            if self.sensor == "SEANAV":
                print(data)
                self.read_NMEA_from_seanav(data)
    def read_NMEA_prop_format(self, data):
        arr = data.decode('utf-8').split(',')
        roll = arr[3]
        pitch = arr[4]
        return (roll, pitch)
    def read_NMEA_from_seanav(self, data):
        my_gps = MicropyGPS()
        for letter in data.decode():
            my_gps.update(letter)
        print("lat: " + str(my_gps.latitude))
        print("lon: " + str(my_gps.longitude))
        print("course: " + str(my_gps.course))
        print("altitude: " + str(my_gps.altitude))
        print("speed: " + str(my_gps.speed))
        print("satellites in use: " + str(my_gps.satellites_in_use))
        print("fix type: " + str(my_gps.fix_type))
        ## 1: no fix, 2: 2d fix, 3: 3d fix




