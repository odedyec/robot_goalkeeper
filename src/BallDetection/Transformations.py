

''' 
Using the camera transformations here 
https://stackoverflow.com/questions/38494485/camera-coordinate-to-pixel-coordinate-opencv
'''

class Transformations:
    def __init__(self, fx=640., fy=640., cx=320., cy=240.):
        self._fx = fx
        self._fy = fy
        self._cx = cx
        self._cy = cy

    def pixel_depth_to_xyz(self, px, z):
        x_prime = (px[0] - self._cx) / self._fx
        y_prime = (px[1] - self._cy) / self._fy
        xyz = (x_prime * z, y_prime * z, z)
        return xyz

    def xyz_to_pixel(self, xyz):
        x_prime = xyz[0] / xyz[2]
        y_prime = xyz[1] / xyz[2]
        u = self._fx * x_prime + self._cx
        v = self._fy * y_prime + self._cy
        return (u, v)


if __name__ == '__main__':
    tf = None 
    import cv2, time
    cap = cv2.VideoCapture(0)
    def mouse_callback(event,x,y,flags,param):
        px = (x, y) 
        if tf is not None:
            print(tf.pixel_depth_to_xyz(px, 0.71))
    while True:
        ret, frame = cap.read()
        if not ret:
            print("failed to grab frame")
            break
        if tf is None:
            tf = Transformations(1.6 * 400, 1.6 * 400, frame.shape[1] / 2, frame.shape[0] / 2)
        cv2.imshow("image", frame)
        cv2.setMouseCallback("image", mouse_callback)
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

    cap.release()
    cv2.destroyAllWindows()
