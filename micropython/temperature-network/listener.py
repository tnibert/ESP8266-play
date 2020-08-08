"""
Simple server to run on receiving machine (not microcontroller)
"""
import socket

PORT = 65432
HOST = '0.0.0.0'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(16)
            print(data.decode(), end="")
            #if not data:
            #    break

# should never reach as we are
print("complete")
