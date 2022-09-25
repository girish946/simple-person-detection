#!python3
from base64 import b64encode, b64decode
import cv2
import websocket
import numpy as np
import json
import sys
import imutils

try:
    import thread
except ImportError:
    import _thread as thread
import time

current_detections = {"list": []}
status_ = {"received": False}


def read_cam(url):
    if url:
        vc = cv2.VideoCapture(url)
        while True:
            # read the frame from rtsp stream
            status, frame = vc.read()
            if status:
                if status_["received"]:
                    if current_detections["list"]:
                        # Draw the bounding boxes
                        for (x, y, w, h) in current_detections["list"][0]:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # Display the frame
                cv2.imshow("img", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    sys.exit(0)


# Receive the data from websocket
def on_message(ws, data):
    if data:
        print("data received")
        dict_op = json.loads(data)

        if len(current_detections["list"]):
            current_detections["list"].pop(0)

        if "detections" in dict_op:
            current_detections["list"].append(dict_op["detections"])
            status_["received"] = True


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    pass


if __name__ == "__main__":
    rtsp_url = sys.argv[1]
    ws_url = sys.argv[2]

    # start reading the frames from rtsp stream in a saparate thread.
    thread.start_new_thread(read_cam, (rtsp_url,))

    # create a websocket connection
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()
