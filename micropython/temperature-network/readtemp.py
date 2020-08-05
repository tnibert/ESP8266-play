from machine import Pin, ADC, I2C
from time import sleep
import ssd1306

# pin constants                                                                                                                                                                              
SCL = 5
SDA = 4
D7 = 13

i2c = I2C(-1, scl=Pin(SCL), sda=Pin(SDA))

width, height = 64, 48
oled = ssd1306.SSD1306_I2C(width, height, i2c)

analog = ADC(0)
digital = Pin(D7, Pin.IN, Pin.PULL_UP)

while True:
  analog_value = analog.read()
  print(analog_value)
  oled.fill(0)
  oled.text(str(analog_value), 0, 0, 1)
  oled.show()
  sleep(0.1)
