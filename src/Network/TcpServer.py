import socket, pickle

PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


class TcpServer:
    def __init__(self, host="0.0.0.0"):
        self._host = host
        self._socket = None
        self._conn = None
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._host, PORT))
        self._socket.listen(1)
        self.wait_for_connection()

    def wait_for_connection(self):
        print('Waitting for client...')
        self._conn, addr = self._socket.accept()
        if self._conn:
            print("Connected by {}".format(addr))
    
    def is_connected(self):
        return self._conn != None

    def disconnect(self):
        if self._conn is None:
            return
        print("Closing conn")
        self._conn.close()
        self._conn = None

    def __del__(self):
        self._socket.close()

    def wait_for_data(self):
        if self._conn is None:
            return None
        data = self._conn.recv(1024)
        if not data:
            self.disconnect()
            return None
        return pickle.loads(data)

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

