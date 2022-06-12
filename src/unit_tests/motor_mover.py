import sys
sys.path.append('../')
sys.path.append('../Network/')
from src.Network.Messages import *
from src.Network.TcpServer import TcpServer


if __name__ == '__main__':
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

