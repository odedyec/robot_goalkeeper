import sys
import os
import pathlib
abs_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(abs_path+'/yolov5/')
import torch.backends.cudnn as cudnn
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.torch_utils import select_device
from yolov5.utils.augmentations import letterbox
from yolov5.utils.general import non_max_suppression, scale_coords
from yolov5.utils.plots import Annotator, colors
from Transformations import Transformations
import numpy as np

whitelist_objects = ['ball', 'orange']

class YoloV5:
    def __init__(self, weights, conf_thresh=0.5, iou_thresh=0.45):
        self.conf_thres = conf_thresh  # confidence threshold
        self.iou_thres = iou_thresh  # NMS IOU threshold
        self._weights = weights
        # Inference
        self._device = select_device('')
        self._model = DetectMultiBackend(self._weights, device=self._device, dnn=False)
        self._stride = self._model.stride
        self._img_size = 640
        self._tf = Transformations()

    def detect(self, cv_img):
        img = letterbox(cv_img, self._img_size, stride=self._stride, auto=True)[0]
        #img = cv_img # letterbox(cv_img, self._img_size, stride=self._stride, auto=True)[0]
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)
        im = torch.from_numpy(img).to(self._device)
        im = im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        pred = self._model(im)
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, None, False, max_det=100)
        results = []
        for i, det in enumerate(pred):  # per image
            if len(det):
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], cv_img.shape).round()
                for *box, conf, cls in reversed(det):
                    c = int(cls)
                    p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
                    res = (p1, p2, conf.item(), self._model.names[c])
                    results.append(res)
        return results

    def clean_results(self, results):
        ans = []
        for res in results:
            p1, p2, conf, label = res
            for lb in whitelist_objects:
                if lb in label:
                    ans.append(res)
        return ans
    
    def get_result_xyz(self, res):
        p1, p2, conf, label = res
        w, h = p2[0] - p1[0], p2[1] - p1[1]
        ball_px_size = (w + h) / 2.  # take avg
        ball_depth = 0.0034 * ball_px_size ** 2 - 1.5735 * ball_px_size + 212.5  # This equation should be revised per ball :(
        px = ((p1[0] + p2[0]) / 2., (p1[1] + p2[1]) / 2.)
        return self._tf.pixel_depth_to_xyz(px, ball_depth / 100.)

    def annotate(self, img, results):
        import cv2
        for res in results:
            p1, p2, conf, label = res
            xyz = self.get_result_xyz(res)
            label += " P: {:.2f}".format(conf) 
            label2 = "({:.1f}, {:.1f}, {:.1f})".format(xyz[0] * 100., xyz[1] * 100., xyz[2] * 100.)
            cv2.rectangle(img, p1, p2, (255, 0, 0), thickness=3, lineType=cv2.LINE_AA)
            tf = 2
            w, h = cv2.getTextSize(label, 0, fontScale=tf / 3, thickness=tf)[0]  # text width, height
            outside = p1[1] - h - 3 >= 0  # label fits outside box
            p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
            cv2.rectangle(img, p1, p2, (255, 0, 0), -1, cv2.LINE_AA)  # filled
            cv2.putText(img, label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2), 0, tf / 3, (255, 255, 255),
                        thickness=tf, lineType=cv2.LINE_AA)
            cv2.putText(img, label2, (p1[0], p1[1] - 20 if outside else p1[1] + h + 2), 0, tf / 3, (255, 255, 255),
                        thickness=tf, lineType=cv2.LINE_AA)


if __name__ == '__main__':
    det = YoloV5('/home/oded/.ivo/yolov5s6.pt', conf_thresh=0.2, iou_thresh=0.2)
    import cv2, time
    cap = cv2.VideoCapture(0)
    writer = None
    while True:
        ret, frame = cap.read()
        if not ret:
            print("failed to grab frame")
            break
        if writer is None:
            h, w, c = frame.shape
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            writer = cv2.VideoWriter("/home/oded/Desktop/ball_track.mp4", fourcc, 30, (w, h))
        start_time = time.time()
        results = det.detect(frame)
        print("Pred took {} sec".format(time.time() - start_time))
        results = det.clean_results(results)
        det.annotate(frame, results)
        writer.write(frame)
        cv2.imshow("yolov5", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

    cap.release()
    writer.release()

    cv2.destroyAllWindows()
    exit(0) 
    img = cv2.imread('/home/oded/Pictures/yolo_test.png', cv2.IMREAD_COLOR)
    for i in range(10):
        start_time = time.time()
        results = det.detect(img)
        print("Pred took {} sec".format(time.time() - start_time))
        det.annotate(img, results)
    cv2.imshow("img_det", img)
    cv2.waitKey(0)
