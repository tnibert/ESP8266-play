"""
Runs on ESP8266
Read from temperature sensor and send to both oled display and remote socket

https://arduinomodules.info/ky-013-analog-temperature-sensor-module/
On my sensor, ground and vcc seem to be switched, which is apparently common
plugged into 3v3
"""
from machine import Pin, ADC, I2C
from time import sleep
from math import log
import ssd1306
import socket
import network

RECONNECT_SLEEP = 5
SEND_SLEEP = 60

# pin constants
SCL = 5
SDA = 4


class OledPrinter:
    def __init__(self):
        self.lineheight = 10

        # oled setup
        i2c = I2C(-1, scl=Pin(SCL), sda=Pin(SDA))
        width, height = 64, 48
        self.oled = ssd1306.SSD1306_I2C(width, height, i2c)

    def display(self, message):
        lines = message.split("\n")
        self.oled.fill(0)

        ypos = 0
        for line in lines:
            self.oled.text(line, 0, ypos, 1)
            ypos += self.lineheight

        self.oled.show()


class Temperature:
    def __init__(self):
        # setup equation to convert resistance to temperature - steinhart-hart equation
        # steinhart-hart coefficients for thermistor
        # these coefficients are bunk, need to find correct values
        self.c1 = 0.001129148
        self.c2 = 0.000234125
        self.c3 = 0.0000000876741
        self.r1 = 10000  # value of R1 on the board?

        # get analog input
        self.analog = ADC(0)

        # populate
        self.read()

    def read(self):
        self.analog_value = self.analog.read()
        print(self.analog_value)

    def convert(self):
        # supposedly this is the steinhart-hart equation which will convert for us
        r2 = self.r1 * (1023.0 / self.analog_value - 1.0)                   # calculate resistance on thermistor
        logr2 = log(abs(r2))                                                # todo: remove abs
        TK = (1.0 / (self.c1 + self.c2 * logr2 + self.c3 * logr2 * logr2 * logr2))  # temperature in Kelvin
        TC = TK - 273.15                                                    # convert Kelvin to Celcius
        print(TC)
        TF = (TC * 9.0) / 5.0 + 32.0                                        # convert Celcius to Farenheit
        return {"K": TK, "C": TC, "F": TF}

    # def output_oled(self, k, c, f):
    #     # output raw value
    #     oled.fill(0)
    #     oled.text(str(self.analog_value), 0, 30, 1)
    #
    #     # output converted values
    #     # oled.fill(0)
    #     oled.text(str(int(k)) + " K", 0, 0, 1)
    #     oled.text(str(int(c)) + " C", 0, 10, 1)
    #     oled.text(str(int(f)) + " F", 0, 20, 1)
    #
    #     oled.show()

    def update(self):
        self.read()
        # to human readable
        #hr = self.convert()
        #self.output_oled(hr["K"], hr["C"], hr["F"])
        return self.analog_value


class Network:
    def do_connect_wifi(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print('connecting to network...')
            self.wlan.connect('essid', 'password')
            while not self.wlan.isconnected():
                pass
        print('network config:', self.wlan.ifconfig())

    def __init__(self):
        # connect to wifi
        self.do_connect_wifi()

        # for socket connection
        self.host = "192.168.1.8"
        self.port = 65432
        self.connect_sock()

    def connect_sock(self):
        self.sock = socket.socket()
        self.sock.connect((self.host, self.port))

    def send(self, msg):
        self.sock.send((str(msg) + "\n").encode())

    def close(self):
        self.sock.close()
        #self.sock.shutdown(socket.SHUT_RDWR)

o = OledPrinter()
t = Temperature()

o.display("Connecting")
try:
    n = Network()
except Exception as e:
    print(e)
    o.display("ConnFail")
    raise e
o.display("Connected")

while True:
    try:
        o.display("try")
        # todo: send an average
        val = t.update()
        o.display(val)
        n.send(val)
        sleep(SEND_SLEEP)
    except OSError as e1:
        o.display("e1")
        print(e1)
        print("Failed to send data over network")
        n.close()
        # try to reconnect
        recon_success = False
        while not recon_success:
            try:
                o.display("recon")
                sleep(RECONNECT_SLEEP)
                n.connect_sock()
            except OSError as e2:
                o.display("e2")
                continue
            except Exception as e3:
                print(e3)
                o.display("e3")
            recon_success = True
