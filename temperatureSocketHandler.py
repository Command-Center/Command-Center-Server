import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from tornado import gen

from sense_hat import SenseHat

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
