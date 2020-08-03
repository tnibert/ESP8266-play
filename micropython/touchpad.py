"""
This script reads from a touch pad connected to pin 13 (D7) and
updates the OLED display with a triangle when touched.
This touch pad:
https://arduinogetstarted.com/tutorials/arduino-touch-sensor
"""

# todo:
# output to web page

from machine import I2C, Pin
import ssd1306

# pin constants
SCL = 5
SDA = 4
D7 = 13

i2c = I2C(-1, scl=Pin(SCL), sda=Pin(SDA))

width, height = 64, 48
oled = ssd1306.SSD1306_I2C(width, height, i2c)

# set initial text
oled.text('Hello,', 0, 0, 1)
oled.text('World!', 0, 10, 1)

def triangle():
    # Draw a triangle and it's centroid
    v1, v2, v3 = (2, 24), (2, 46), (60, 46)
    oled.vline(v1[0], v1[1], v2[1] - v1[1], 1)
    oled.hline(v2[0], v2[1], v3[0] - v2[0], 1)
    oled.line(v1[0], v1[1], v3[0], v3[1], 1)
    oled.pixel((v1[0] + v2[0] + v3[0]) // 3, (v1[1] + v2[1] + v3[1]) // 3, 1)

oled.show()

# in most cases only pins 0, 2, 4, 5, 12, 13, 14, 15, and 16 can be used
# https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/
p = Pin(D7, Pin.IN, Pin.PULL_UP)

# for hard interrupt
def callback(mypin):
    curval = mypin.value()
    oled.fill(0)
    if curval == 0:
        print("Pad released")
        oled.text('Hello,', 0, 0, 1)
        oled.text('World!', 0, 10, 1)
    elif curval == 1:
        print("Pad touched")
        oled.text('Touch!', 0, 0, 1)
        triangle()
    oled.show()

# it looks like you can't set up two irqs
p.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)
