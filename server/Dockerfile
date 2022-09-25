FROM ubuntu:20.04
ENV TZ=Asia/Kolkata \
    DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y gcc \
        python3-dev \
        python3 \
        python3-pip \
        curl \
        git \
        unzip \
        sudo \
        ffmpeg \
        libsm6 \
        libxext6 \
        vim

WORKDIR /simple-person-detection


COPY . ./

RUN pip install -r requirements.txt

CMD ["/bin/bash", "-c", "start-services.sh"]
