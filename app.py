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
import simplejson as json

# import temperatureSocketHandler as TemperatureSocketHandler

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
        print("ASYNC FUNC CALLED: IRTEMP")
        while(self.sending):
            print("test")
            try:
                self.instrument = minimalmodbus.Instrument('/dev/ttyUSB-IR1', 1)
                self.instrument.serial.baudrate = 9600
                temp = round(self.instrument.read_register(16, 1), 1)
                yield self.write_message(str(temp))
                yield gen.sleep(5)
            except Exception as ex:
                yield gen.sleep(1)
                pass
    def open(self):
        print("IRTemperature socket opened")
        self.instrument = minimalmodbus.Instrument('/dev/ttyUSB-IR1', 1)
        self.instrument.serial.baudrate = 9600
        self.sending = True
    def on_message(self, message):
        print("ON_MESSAGE: IRTEMP")
        if(message == "START"):
            self.instrument = minimalmodbus.Instrument('/dev/ttyUSB-IR1', 1)
            self.instrument.serial.baudrate = 9600
            tornado.ioloop.IOLoop.current().add_future(self.async_write(), lambda f: self.close())
        if(message == "STOP"):
            self.sending = False
    def on_close(self):
        print("IRTemperature socket closed")
        self.sending = False
class IR2TemperatureSocketHandler(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def async_write(self):
        print("ASYNC FUNC CALLED: IR2TEMP")
        while(self.sending):
            try:
                self.instrument = minimalmodbus.Instrument('/dev/ttyUSB-IR2', 1)
                self.instrument.serial.baudrate = 9600
                temp = round(self.instrument.read_register(16, 1), 1)
                yield self.write_message(str(temp))
                yield gen.sleep(5)
            except Exception as ex:
                yield gen.sleep(1)
                pass
    def open(self):
        print("IR2Temperature socket opened")
        self.instrument = minimalmodbus.Instrument('/dev/ttyUSB-IR2', 1)
        self.instrument.serial.baudrate = 9600
        self.sending = True
    def on_message(self, message):
        print("ON_MESSAGE: IR2TEMP")
        if(message == "START"):
            self.instrument = minimalmodbus.Instrument('/dev/ttyUSB-IR2', 1)
            self.instrument.serial.baudrate = 9600
            tornado.ioloop.IOLoop.current().add_future(self.async_write(), lambda f: self.close())
        if(message == "STOP"):
            self.sending = False
    def on_close(self):
        print("IR2Temperature socket closed")
        self.sending = False
class HumiditySocketHandler(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def async_write(self):
        print("HUMIDITY ASYNC FUNC CALLED")
        while(self.sending):
            humidity = round(self.sense.get_humidity(), 1)
            yield self.write_message(str(humidity))
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
            pitch = str(round(orientation["pitch"], 0))
            roll = str(round(orientation["roll"], 0))
            yaw = str(round(orientation["yaw"], 0))
            orientations = pitch + " " + roll + " " + yaw
            yield self.write_message(orientations)
            yield gen.sleep(0.01)
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
            x = str(round(acceleration['x'], 1))
            y = str(round(acceleration['y'], 1))
            z = str(round(acceleration['z'], 1))

            accelerations = x + " " + y + " " + z
            yield self.write_message(accelerations)
            yield gen.sleep(0.01)
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
                yield self.write_message(json.dumps(self.create_dict_from_response(packet)))
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
    def create_dict_from_response(self, packet):
        #Exception her? if setninger på mode.
        dict = {}
        dict['mode'] = str(packet.mode)
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
            (r'/irtemp2', IR2TemperatureSocketHandler),
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



