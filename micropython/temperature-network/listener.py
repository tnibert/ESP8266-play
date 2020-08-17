#! /usr/bin/env python3
"""
Simple server to run on receiving machine (not microcontroller)
Receive temperature values from ESP8266 over HTTP
"""
from datetime import datetime
from flask import Flask, request

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

PORT = 8080
HOST = '0.0.0.0'

app = Flask(__name__)


@app.route('/tempreceive', methods=['POST'])
def receive_data():
    print("{time}::{value}".format(time=datetime.now(), value=request.get_json().get("value")))
    return 'received'

if __name__ == '__main__':
    app.run(HOST, PORT, debug=True)
