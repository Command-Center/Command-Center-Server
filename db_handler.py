from influxdb import InfluxDBClient
import simplejson as json
from point import Point
import config as cfg

class DBHandler():
    def __init__(self, local=True, cloud=True):
        self.local = local
        self.cloud = cloud
        self.clients = []
        if local:
            self.client_local = InfluxDBClient(database='OLCC')
            self.clients.append(self.client_local)
        if cloud:
            self.client_cloud = InfluxDBClient(host=cfg.ip_influxdb_cloud, port=cfg.port_influxdb, database='OLCC')
            self.clients.append(self.client_cloud)
    def add_to_db(self, message, topic):
        for c in self.clients:
            try:
                c.write_points(self.create_json_point(message, topic))
            except Exception as e:
                print("Write error: " + str(e))
    def create_json_point(self, message, topic):
        point = Point(topic, message)
        point_json = [point.__dict__]
        return point_json

