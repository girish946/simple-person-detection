# Simple-Person-detection Server

# prerequisites

- [Docker](https://www.docker.com/)

# Building docker image

```
docker build . -t simple-person-detection
```

# Usage

```
docker run --rm -it -e RTSP_PROTOCOLS=tcp -e RTSP_URL=<RTSP_URL>  -p 8005:8005 simple-person-detection
```
