#!/bin/sh
python3 -u /simple-person-detection/websocket_server.py&
sleep 2
python3 -u /simple-person-detection/detection.py -u $RTSP_URL

