from datetime import datetime
import socket
import sys
import threading
import time
import dht11
from influxdb import InfluxDBClient
import RPi.GPIO as GPIO


class sensor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.kill_received = False
        self.temperature = 0
        self.humidity = 0
        self.instance = self.initialize_gpio()
        self.interval = 5

    def initialize_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        return dht11.DHT11(pin=14)

    def run(self):
        while not self.kill_received:
            self.sensing()
            time.sleep(self.interval)

    def sensing(self):
        result = self.instance.read()
        if result.is_valid():
            print('.', end='')
            sys.stdout.flush()
            self.temperature = result.temperature
            self.humidity = result.humidity


def get_hostip():
    """ thanks. https://qiita.com/kjunichi/items/8e4967d04c3a1f6af35e """
    return [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close())
            for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


def send_data(client, host):
    while True:
        try:
            insert_data(client, s.temperature, s.humidity, host)
            time.sleep(30)
        except KeyboardInterrupt:
            s.kill_received = True
            break
    print('\nfin')


def insert_data(client, temp, humi, host):
    json_body = [{'measurement': 'dht11',
                  'tags': {'host': host},
                  'time': datetime.now().isoformat(),
                  'fields': {'temperature': temp, 'humidity': humi}}]
    print(json_body)
    print(client.write_points(json_body))


if __name__ == '__main__':
    s = sensor()
    s.start()
    client = InfluxDBClient(host='10.0.1.6', port=8086, database='raspberrypi')
    send_data(client, get_hostip())
    client.close()
