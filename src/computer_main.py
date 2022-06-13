import sys
sys.path.append('./Network/')
sys.path.append('./BallDetection/')
sys.path.append('./')
import tty
import time
import math
from BallDetection.YoloV5 import YoloV5
from Network.TcpClient import TcpClient
from Messages import MotorAngle
import cv2, time


def deg_to_rad(val):
    return math.pi / 180. * val


if __name__ == '__main__':
    client = TcpClient("192.168.0.112")
    det = YoloV5('/home/oded/.ivo/yolov5s6.pt', conf_thresh=0.2, iou_thresh=0.2)
    cap = cv2.VideoCapture(0)
    try:
        mot_angle = MotorAngle()
        angle = 0.    
        while True:
            if not client.is_connected():
                client.wait_for_connection()
            ret, frame = cap.read()
            if not ret:
                print("failed to grab frame")
                break
            results = det.detect(frame)
            results = det.clean_results(results)
            det.annotate(frame, results)
            cv2.imshow("yolov5", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            if len(results):
                xyz = det.get_result_xyz(results[0])
                xyz = list(xyz)
                xyz[0] += 0.22
                angle = math.atan2(-xyz[0], xyz[1])
                if angle > math.pi / 2.:
                    angle = math.pi / 2.
                if angle < -math.pi / 2.:
                    angle = -math.pi / 2.
            else:
                angle = 0
            mot_angle.angle = angle
            client.send_data(mot_angle)
    
    finally:
        client.disconnect()
        cap.release()
        cv2.destroyAllWindows()

