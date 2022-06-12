import time
import socket, pickle

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

class TcpClient:
    def __init__(self, host=HOST):
        self._host = host
        self._socket = None
        self.wait_for_connection()

    def wait_for_connection(self):
        while True:
            try:            
                print('Waitting for server...')
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._socket.connect((self._host, PORT))
                break
            except:
                time.sleep(1)
    
    def is_connected(self):
        return self._socket != None

    def disconnect(self):
        self._socket.close()
        self._socket = None

    def send_data(self, obj):
        if self._socket:
            data_string = pickle.dumps(obj)
            try:
                self._socket.send(data_string)
            except:
                self.disconnect()

if __name__ == '__main__':
    from Messages import *
    client = TcpClient()
    angle = -3.14159
    try:
        while True:
            if not client.is_connected():
                client.wait_for_connection()
            mot_angle = MotorAngle()
            mot_angle.angle = angle
            client.send_data(mot_angle)
            time.sleep(.1)
            angle += 0.1
    finally:
        client.disconnect()


