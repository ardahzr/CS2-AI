import cv2
#import dxcam
from ultralytics import YOLO
import win32api
import win32con
from windowcapture import WindowCapture
import os
import numpy as np
from time import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))
wincap = WindowCapture()

print("Loading model...")
model = YOLO("best.pt")
crosshair = win32api.GetCursorPos()
print("Starting camera...")
loop_time = time()

while True:
    frame = wincap.get_screenshot()
    resized_frame = cv2.resize(frame, (1280, 720))
    results = model.predict(frame)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()
 
    for result in results:
        for box, label in zip(result.boxes.xyxy, result.boxes.cls):
            x1, y1, x2, y2 = box.int().tolist()
            color = (
                (0, 255, 0) if label == 1 else (0, 0, 255)
            )  

            if label == 1 or label == 0:

                center = (
                    int(x1 * 1280 / resized_frame.shape[1]) + int(x2 * 1280 / resized_frame.shape[1])
                ) / 2, (
                    int(y1 * 720 / resized_frame.shape[0]) + int(y2 * 720 / resized_frame.shape[0])
                ) / 2

                
                center = (
                    int(center[0] * resized_frame.shape[1] / 1280),
                    int(center[1] * resized_frame.shape[0] / 720),
                )

                anlik = win32api.GetCursorPos()

                yolx = center[0] - anlik[0]    
                yoly = center[1] - anlik[1]

                cv2.arrowedLine(
                    resized_frame,
                    (
                        int(crosshair[0] * 1280 / frame.shape[1]),
                        int(crosshair[1] * 720 / frame.shape[0]),
                    ),
                    (int(center[0]), int(center[1])),
                    (255, 0, 0),
                    thickness=2,
                )
                
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,yolx,yoly+10,0,0,)
                if (
                    crosshair[0] > x1
                    and crosshair[0] < x2
                    and crosshair[1] > y1
                    and crosshair[1] < y2
                ):
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                

    cv2.imshow("frame", resized_frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()