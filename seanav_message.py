class SeanavMessage(object):
    def __init__(self, timestamp, packet):
        self.latitude = packet.latitude_string()
        self.longitude = packet.longitude_string()
        self.course = packet.course
        self.speed = packet.speed_string()
        self.altitude = packet.altitude
        self.satellites_in_use = packet.satellites_in_use
        self.fix = packet.fix_type
        self.timestamp = timestamp

