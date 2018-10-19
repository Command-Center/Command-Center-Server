import socket
import threading
import time
import binascii
import datetime
import queue
import simplejson as json


class UDPReceiver(threading.Thread):
    def __init__(self, ip, port, queue):
        threading.Thread.__init__(self)
        self.port = port
        self.ip = ip
        self.queue = queue
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.ip, self.port))
    def run(self):
        while 1:
            ## How to decide size?
            data, addr = self.s.recvfrom(100)
            res = self.read_NMEA_prop_format(data)
            dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            message = {"timestamp": dt, "pitch" : res[1], "roll" : res[0]}
            json_object = json.dumps(message)
            topic = "orientation_imu"
            queue_object = [ topic, json_object, message ]
            self.queue.put(queue_object)
            time.sleep(0.3)
    def read_NMEA_prop_format(self, data):
        arr = data.decode('utf-8').split(',')
        roll = arr[3]
        pitch = arr[4]
        return (roll, pitch)
