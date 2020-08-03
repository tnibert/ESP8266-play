"""
This script reads from a touch pad connected to pin 4 (D2)
This touch pad:
https://arduinogetstarted.com/tutorials/arduino-touch-sensor
"""

from machine import Pin

# in most cases only pins 0, 2, 4, 5, 12, 13, 14, 15, and 16 can be used
# https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/
p = Pin(4, Pin.IN, Pin.PULL_UP)

# for hard interrupt
def callback(mypin):
    curval = mypin.value()
    if curval == 0:
        print("Pad released")
    elif curval == 1:
        print("Pad touched")

# it looks like you can't set up two irqs
p.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)
