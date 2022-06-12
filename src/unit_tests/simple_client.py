import sys
sys.path.append('../')
sys.path.append('../Network/')
import time
from src.Network.Messages import *
from src.Network.TcpClient import TcpClient
if __name__ == '__main__':
    client = TcpClient("192.168.0.112")
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

