"""
https://arduinomodules.info/ky-013-analog-temperature-sensor-module/

https://forum.arduino.cc/index.php?topic=406890.0 -
If you look at module faced with pins down it says S, GND, VCC but it is not actually, proper order is VCC, GND, S.
^ todo: confirm
"""
from machine import Pin, ADC, I2C
from time import sleep
from math import log
import ssd1306

# pin constants                                                                                                                                                                              
SCL = 5
SDA = 4

# oled setup
i2c = I2C(-1, scl=Pin(SCL), sda=Pin(SDA))
width, height = 64, 48
oled = ssd1306.SSD1306_I2C(width, height, i2c)

# get analog input
analog = ADC(0)

# setup equation to convert resistance to temperature - steinhart-hart equation
# steinhart-hart coefficients for thermistor
# these coefficients are bunk, need to find correct values
c1 = 0.001129148
c2 = 0.000234125
c3 = 0.0000000876741
r1 = 10000                                                  # value of R1 on the board?

while True:
    analog_value = analog.read()
    print(analog_value)

    # output raw value
    oled.fill(0)
    oled.text(str(analog_value), 0, 30, 1)

    # supposedly this is the steinhart-hart equation which will convert for us
    r2 = r1 * (1023.0 / analog_value - 1.0)                 # calculate resistance on thermistor
    logr2 = log(abs(r2))                                    # todo: remove abs
    TK = (1.0 / (c1 + c2*logr2 + c3*logr2*logr2*logr2))     # temperature in Kelvin
    TC = TK - 273.15                                        # convert Kelvin to Celcius
    print(TC)
    TF = (TC * 9.0)/ 5.0 + 32.0                             # convert Celcius to Farenheit

    # output converted values
    #oled.fill(0)
    oled.text(str(int(TK)) + " K", 0, 0, 1)
    oled.text(str(int(TC)) + " C", 0, 10, 1)
    oled.text(str(int(TF)) + " F", 0, 20, 1)

    oled.show()

    sleep(0.1)
