import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from tornado import gen

from sense_hat import SenseHat
import time

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
            temp = self.sense.get_temperature()
            yield self.write_message(str(temp))
            print(str(temp))
            yield gen.sleep(2)
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
class HumiditySocketHandler(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def async_write(self):
        print("HUMIDITY ASYNC FUNC CALLED")
        while(self.sending):
            humidity = self.sense.get_humidity()
            yield self.write_message(str(humidity))
            print(str(humidity))
            yield gen.sleep(2)
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
        print("Humidity" socket closed")
        self.sending = False
class PressureSocketHandler(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def async_write(self):
        print("PRESSURE ASYNC FUNC CALLED")
        while(self.sending):
            pressure = self.sense.get_pressure()
            yield self.write_message(str(pressure))
            print(str(pressure))
            yield gen.sleep(2)
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
            pitch = str(orientation["pitch"])
            roll = str(orientation["roll"])
            yaw = str(orientation["yaw"])

            orientations = pitch + " " + roll + " " + yaw
            yield self.write_message(orientations)
            yield gen.sleep(2)
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
            acceleration = sense.get_accelerometer_raw()
            x = str(acceleration['x'])
            y = str(acceleration['y'])
            z = str(acceleration['z'])

            accelerations = x + " " + y + " " + z
            yield self.write_message(accelerations)
            yield gen.sleep(2)
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
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler),
            (r'/temp', TemperatureSocketHandler),
            (r'/pressure', PressureSocketHandler),
            (r'/humidity', HumiditySocketHandler),
            (r'/orientation', OrientationSocketHandler),
            (r'/acceleration', AccelerationSocketHandler)
        ]

        settings = {
            'template_path': 'templates'
            }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    print("Server running...")
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
