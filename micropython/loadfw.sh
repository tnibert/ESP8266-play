#! /bin/bash
# download and load micropython firmware onto ESP8266
set -e
fi="esp8266-20191220-v1.12.bin"
wget http://micropython.org/resources/firmware/$fi
# pip3 install esptool
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 $fi
