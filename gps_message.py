class GpsMessage(object):
    def __init__(self, timestamp, packet):
        self.timestamp = timestamp
        self.mode = packet.mode
        self.lat = packet.lat
        self.lon = packet.lon
        self.hspeed = packet.hspeed
        if packet.mode >= 3
            self.alt = packet.alt
            self.climb = packet.climb