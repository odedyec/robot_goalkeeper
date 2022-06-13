import os, sys
abs_path = os.path.dirname(os.path.abspath(__file__))
print(abs_path)
sys.path.append(abs_path+'/../')
sys.path.append(abs_path+'/../Network/')
import select
import tty
import termios
import time
import math
from Network.TcpServer import TcpServer
from Messages import MotorAngle
from MotorHandler import MotorHandler

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
