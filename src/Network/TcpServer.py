import socket, pickle

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


class TcpServer:
    def __init__(self):
        self._socket = None
        self._conn = None
        self.wait_for_connection()

    def wait_for_connection(self):
        print('Waitting for client...')
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((HOST, PORT))
        self._socket.listen()
        self._conn, addr = self._socket.accept()
        if self._conn:
            print(f"Connected by {addr}")
    
    def is_connected(self):
        return self._socket != None

    def disconnect(self):
        self._conn.close()
        self._socket.close()
        self._socket = None
        self._conn = None

    def wait_for_data(self):
        data = self._conn.recv(1024)
        if not data:
            self.disconnect()
            return None
        return pickle.loads(data, fix_imports=False, errors='')

if __name__ == '__main__':
    from Messages import *
    server = TcpServer()
    try:
        while True:
            if not server.is_connected():
                server.wait_for_connection()
            data = server.wait_for_data()
            if type(data) == MotorAngle:
                print(data.angle)
            else:
                print(data)
    finally:
        server.disconnect()

