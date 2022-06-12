import sys
sys.path.append('../Network/')
sys.path.append('../')
import select
import tty
import termios
import time
import math
from src.Network.TcpServer import TcpServer
from src.Network.Messages import MotorAngle
from src.MotorHandler import MotorHandler

if __name__ == '__main__':
    server = TcpServer()
    try:
        mot = MotorHandler()
        while True:
            if not server.is_connected():
                server.wait_for_connection()
            data = server.wait_for_data()
            if type(data) == MotorAngle:
                mot.set_angle(data.angle)
                print(data.angle)
            else:
                print(data)

    except KeyboardInterrupt:
        pass #GPIO.cleanup()
    finally:
        server.disconnect()
