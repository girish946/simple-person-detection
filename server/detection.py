#!python3
from imutils.video import VideoStream
import base64
import websocket
import cv2
import imutils
import sys
import json
import numpy as np
import argparse
import cv2

cv2.useOptimized()

model = "MobileNetSSD_deploy.caffemodel"
proto = "MobileNetSSD_deploy.prototxt.txt"

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = [
    "person"
]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", required=True, help="URL for the video")
ap.add_argument(
    "-c",
    "--confidence",
    type=float,
    default=0.2,
    help="minimum probability to filter weak detections",
)
args = vars(ap.parse_args())

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(proto, model)

img = {"img": np.zeros(255)}

ws = []

def init_connection():
    try:
        ws.append(websocket.WebSocket())
        ws[0].connect("ws://127.0.0.1:8005/in")
    except Exception as e:
        print(e)
        sys.exit(1)


def detect(image):
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5
    )

    # pass the blob through the network and obtain the detections and
    # predictions
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()
    boxes = []

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            boxes.append([int(startX), int(startY), int(endX), int(endY)])

            # display the prediction
            try:
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                print("[INFO] {}".format(label))
                cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(
                    image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2
                )
            except Exception as e:
                pass

    # send the detections over websocket
    data = json.dumps({"detections": boxes})
    print(data)
    ws[0].send(data)


def start(url):
    cap = VideoStream(url).start()
    print("device init-success")
    while True:
        try:
            frame = cap.read()
            if type(frame) is np.ndarray:
                detect(frame)
            else:
                pass
        except KeyboardInterrupt as ke:
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    init_connection()
    start(args["url"])
