import sys
sys.path.append('../Network/')
sys.path.append('../')
import select
import tty
import termios
import time
import math
from src.Network.TcpClient import TcpClient
from src.Network.Messages import MotorAngle


def deg_to_rad(val):
    return math.pi / 180. * val


def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


if __name__ == '__main__':
    old_settings = termios.tcgetattr(sys.stdin)
    client = TcpClient()
    try:
        tty.setcbreak(sys.stdin.fileno())
        mot_angle = MotorAngle()
        angle = 0.    
        while True:
            if not client.is_connected():
                client.wait_for_connection()
            time.sleep(0.05)  # work at 20Hz
            if isData():
                c = sys.stdin.read(1)
                if c == 'a':
                    angle -= 5
                elif c == 'd':
                    angle += 5
                elif c == 's':
                    angle = 0.

                if angle > 90:
                    angle = 90
                elif angle < -90:
                    angle = -90
                print(c, angle)


                if c == '\x1b':         # x1b is ESC
                    break
            mot_angle.angle = deg_to_rad(angle)
            client.send_data(mot_angle)
    
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        client.disconnect()

