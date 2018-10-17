import paho.mqtt.client as mqtt
import threading
import time
import queue
from sense_hat import SenseHat
from message_sender import MessageSender
from mqtt_connector import MqttConnector
from sensors.temperature_sensor import TemperatureSensor
from sensors.ir_temp_sensor import IRTemperatureSensor
from sensors.ir2_temp_sensor import IR2TemperatureSensor
from sensors.gps_sensor import GpsSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.pressure_sensor import PressureSensor
from sensors.orientation_sensor import OrientationSensor
from sensors.acceleration_sensor import AccelerationSensor


# from sense_hat import SenseHat

def main():
    running = True
    message_queue = queue.Queue()
    
    
    print("Creating mqtt class..")
    mqtt_thread = MqttConnector()
    mqtt_thread.start()

    ## Start sensors
    temp_sensor = TemperatureSensor(message_queue)
    #ir_temp_sensor = IRTemperatureSensor(message_queue)
    #ir2_temp_sensor = IR2TemperatureSensor(message_queue)
    #gps_sensor = GpsSensor(message_queue)
    humidity_sensor = HumiditySensor(message_queue)
    pressure_sensor = PressureSensor(message_queue)
    orientation_sensor = OrientationSensor(message_queue)
    acceleration_sensor = AccelerationSensor(message_queue)

    temp_sensor.start()
    ir_temp_sensor.start()
    ir2_temp_sensor.start()
    humidity_sensor.start()
    pressure_sensor.start()
    orientation_sensor.start()
    acceleration_sensor().start()


    
    ## Wait for connected to server
    while not mqtt_thread.connected:
        continue

    print("Connected...")
    print("Start message sender")
    sender = MessageSender(message_queue, mqtt_thread)
    sender.run()

    ## Keep from stopping program
    while(running):
        continue

    
    print("Program end")
if __name__ == "__main__":
    main()

