import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from tornado import gen

from sense_hat import SenseHat
import time
import minimalmodbus
import gpsd
import subprocess
import json


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass
    def on_message(self, message):
        for i in range(4):
            self.write_message("your message was: " + str(i))
    def on_close(self):
        pass
class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
       self.render("index.html")
class TemperatureSocketHandler(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def async_write(self):
        print("ASYNC FUNC CALLED")
        while(self.sending):
            temp = round(self.sense.get_temperature(), 1)
            yield self.write_message(str(temp))
            print(str(temp))
            yield gen.sleep(5)
    def open(self):
        print("Temperature socket opened")
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = False
    def on_message(self, message):
        print("ON_MESSAGE: TEMP")
        if(message == "START"):
            self.sending = True
            tornado.ioloop.IOLoop.current().add_future(self.async_write(), lambda f: self.close())
        if(message == "STOP"):
            self.sending = False
    def on_close(self):
        print("temperature socket closed")
        self.sending = False
class IRTemperatureSocketHandler(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def async_write(self):
        print("ASYNC FUNC CALLED")
        while(self.sending):
            try:
                temp = round(self.instrument.read_register(16, 1), 1)
                yield self.write_message(str(temp))
                yield gen.sleep(5)
            except Exception:
                yield gen.sleep(5)
                pass
    def open(self):
        print("IRTemperature socket opened")
        self.instrument = minimalmodbus.Instrument('/dev/ttyUSB-IR1', 1)
        self.instrument.baudrate = 9600
        self.sending = False
    def on_message(self, message):
        print("ON_MESSAGE: TEMP")
        if(message == "START"):
            self.sending = True
            tornado.ioloop.IOLoop.current().add_future(self.async_write(), lambda f: self.close())
        if(message == "STOP"):
            self.sending = False
    def on_close(self):
        print("IRTemperature socket closed")
        self.sending = False
class HumiditySocketHandler(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def async_write(self):
        print("HUMIDITY ASYNC FUNC CALLED")
        while(self.sending):
            humidity = round(self.sense.get_humidity(), 1)
            yield self.write_message(str(humidity))
            print(str(humidity))
            yield gen.sleep(10)
    def open(self):
        print("Humidity socket opened")
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = False
    def on_message(self, message):
        print("ON_MESSAGE: HUM")
        if(message == "START"):
            self.sending = True
            tornado.ioloop.IOLoop.current().add_future(self.async_write(), lambda f: self.close())
        if(message == "STOP"):
            self.sending = False
    def on_close(self):
        print("Humidity socket closed")
        self.sending = False
class PressureSocketHandler(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def async_write(self):
        print("PRESSURE ASYNC FUNC CALLED")
        while(self.sending):
            pressure = round(self.sense.get_pressure(), 1)
            yield self.write_message(str(pressure))
            print(str(pressure))
            yield gen.sleep(10)
    def open(self):
        print("Pressure socket opened")
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = False
    def on_message(self, message):
        print("ON_MESSAGE: PRESSURE")
        if(message == "START"):
            self.sending = True
            tornado.ioloop.IOLoop.current().add_future(self.async_write(), lambda f: self.close())
        if(message == "STOP"):
            self.sending = False
    def on_close(self):
        print("Pressure socket closed")
        self.sending = False
class OrientationSocketHandler(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def async_write(self):
        print("ORIENTATION ASYNC FUNC CALLED")
        while(self.sending):
            orientation = self.sense.get_orientation()
            pitch = str(round(orientation["pitch"], 1))
            roll = str(round(orientation["roll"], 1))
            yaw = str(round(orientation["yaw"], 1))

            orientations = pitch + " " + roll + " " + yaw
            yield self.write_message(orientations)
            yield gen.sleep(0.25)
    def open(self):
        print("Orientation socket opened")
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = True
    def on_message(self, message):
        print("ON_MESSAGE: ORIENTATION")
        if(message == "START"):
            self.sending = True
            tornado.ioloop.IOLoop.current().add_future(self.async_write(), lambda f: self.close())
        if(message == "STOP"):
            self.sending = False
    def on_close(self):
        self.sending = False
class AccelerationSocketHandler(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def async_write(self):
        print("ACCELERATION ASYNC FUNC CALLED")
        while(self.sending):
            acceleration = self.sense.get_accelerometer_raw()
            x = str(round(acceleration['x'], 2))
            y = str(round(acceleration['y'], 2))
            z = str(round(acceleration['z'], 2))

            accelerations = x + " " + y + " " + z
            yield self.write_message(accelerations)
            yield gen.sleep(0.25)
    def open(self):
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = True
    def on_message(self, message):
        print("ON_MESSAGE: ACCELERATION")
        if(message == "START"):
            self.sending = True
            tornado.ioloop.IOLoop.current().add_future(self.async_write(), lambda f: self.close())
        if(message == "STOP"):
            self.sending = False
    def on_close(self):
        self.sending = False
class GPSSocketHandler(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def async_write(self):
        print("ASYNC FUNC CALLED")
        first_fix = False
        while(self.sending):
            try:
                packet = gpsd.get_current()
                yield self.write_message(JSONEncoder().encode(create_dict_from_response(packet)))
                first_fix = True
            except Exception as e:
                print("GPS FEIL: " + str(e))
            if first_fix:
                yield gen.sleep(5)
            else:
                yield gen.sleep(1)
    def open(self):
        print("GPS socket opened")
        gpsd.connect()
        self.sending = False
    def on_message(self, message):
        print("ON_MESSAGE: TEMP")
        if(message == "START"):
            self.sending = True
            tornado.ioloop.IOLoop.current().add_future(self.async_write(), lambda f: self.close())
        if(message == "STOP"):
            self.sending = False
    def on_close(self):
        print("GPS socket closed")
        self.sending = False
    def create_dict_from_response(packet):
        #Exception her? if setninger på mode.
        dict = {}
        dict['lat'] = str(packet.lat)
        dict['lon'] = str(packet.lon)
        dict['hspeed'] = str(packet.hspeed)
        if packet.mode >= 3:
            dict['alt'] = str(packet.alt)
            dict['climb'] = str(packet.climb)
        return dict

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler),
            (r'/temp', TemperatureSocketHandler),
            (r'/pressure', PressureSocketHandler),
            (r'/humidity', HumiditySocketHandler),
            (r'/orientation', OrientationSocketHandler),
            (r'/acceleration', AccelerationSocketHandler),
            (r'/irtemp', IRTemperatureSocketHandler),
            (r'/gps', GPSSocketHandler)
        ]

        settings = {
            'template_path': 'templates'
            }
        tornado.web.Application.__init__(self, handlers, **settings)

def start_gpsd():
    killall = "sudo killall gpsd"
    stop = "sudo systemctl stop gpsd.socket"
    disable = "sudo systemctl disable gpsd.socket"
    start = "sudo gpsd /dev/ttyUSB-GPS -F /var/run/gpsd.sock"
    c = killall + "; " + stop + "; " + disable + "; " + start
    process = subprocess.Popen(c, stdout=subprocess.PIPE, shell=True)
    proc = process.communicate()

if __name__ == '__main__':
    start_gpsd()
    print("Server running...")
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()



