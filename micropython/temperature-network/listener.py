#! /usr/bin/env python3
"""
Simple server to run on receiving machine (not microcontroller)
"""
from datetime import datetime
from flask import Flask, request

PORT = 8080
HOST = '0.0.0.0'

app = Flask(__name__)


@app.route('/', methods=['POST'])
def receive_data():
    print(request.data)
    return ''
    #print("{time}::{value}".format(time=datetime.now(), value=val))

if __name__ == '__main__':
    app.run(HOST, PORT, debug=True)
