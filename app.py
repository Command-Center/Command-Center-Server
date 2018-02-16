import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop

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
    def open(self):
        print("Temperature socket opened")
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = False
    def on_message(self, message):
        num = 0
        message = message.strip(' \t\n\r')
        print(message)
        mes = [elem.encode("hex") for elem in message]
        i = 0
        for idx, x in enumerate(reversed(mes)):
            if x != "00":
                i = idx
                break
        mes = mes[:(len(mes)-i)]
        for x in mes:
             print(x)
        if(message == "START"):
            print("Inside start if")
            self.sending = True
        if(message == "STOP"):
            self.sending = False
        while(self.sending):            
            num = num + 1
            temp = self.sense.get_temperature()
            self.write_message(str(temp))
            print("temperature: " + str(temp))
            time.sleep(0.5)
    def on_close(self):
        print("temperature socket closed")
        self.sending = False
class HumiditySocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = True
    def on_message(self, message):
        num = 0
        while(self.sending and num < 10):
            num = num + 1
            humidity = self.sense.get_humidity()
            self.write_message(str(humidity))
            time.sleep(2)
    def on_close(self):
        self.sending = False
class PressureSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = True
    def on_message(self, message):
        num = 0
        while(self.sending and num < 10):
            num = num + 1
            pressure = self.sense.get_pressure()
            self.write_message(str(pressure))
            time.sleep(2)
    def on_close(self):
        self.sending = False
class OrientationSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = True
    def on_message(self, message):
        num = 0
        while(self.sending and num < 10):
            num = num + 1
            orientation = self.sense.get_orientation()
            pitch = str(orientation["pitch"])
            roll = str(orientation["roll"])
            yaw = str(orientation["yaw"])

            orientations = pitch + " " + roll + " " + yaw
            self.write_message(orientations)
            time.sleep(0.1)
    def on_close(self):
        self.sending = False
class AccelerationSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.sense = SenseHat()
        self.sense.clear()
        self.sending = True
    def on_message(self, message):
        num = 0
        while(self.sending and num < 10):
            num = num + 1
            acceleration = sense.get_accelerometer_raw()
            x = str(acceleration['x'])
            y = str(acceleration['y'])
            z = str(acceleration['z'])

            accelerations = x + " " + y + " " + z
            self.write_message(accelerations)
            time.sleep(0.1)
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
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

