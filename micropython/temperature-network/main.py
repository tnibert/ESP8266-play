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
SEND_SLEEP = 1

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

    def display(self, message, start=0):
        lines = str(message).split("\n")
        self.oled.fill(0)

        ypos = start
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

    def update(self):
        self.read()
        # to human readable
        #hr = self.convert()
        #self.output_oled(hr["K"], hr["C"], hr["F"])
        return self.analog_value


def http_post(url, port, data):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)

    # todo: this is wrong, fix
    post_text = 'POST %s HTTP/1.1\r\nHost: %s\r\nContent-Type: application/json\r\nContent-Length: %s\r\n\r\n{"value": "%s"}' % (path, host, str(13+len(str(data))), str(data))

    s.send(bytes(post_text, 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()


def do_connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('essid', 'password')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    return wlan


o = OledPrinter()
t = Temperature()

o.display("Connecting")
try:
    w = do_connect_wifi()
except Exception as e:
    print(e)
    o.display("ConnFail")
    raise e
o.display("Connected")

while True:
    # todo: send an average
    val = t.update()
    o.display(val)
    try:
        http_post("http://192.168.1.8/", 8080, val)
    except Exception as e:
        print(e)
        o.display("{}\nSENDFAIL".format(val))

    sleep(SEND_SLEEP)
