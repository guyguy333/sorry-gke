FROM python:3.9-alpine

RUN apk update && \
  apk add -f curl bash gcc musl-dev && \
  rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install kubernetes pyyaml kopf

RUN addgroup -g 1000 -S hiventive && \
    adduser -u 1000 -S hiventive -G hiventive -h /home/hiventive

USER 1000
WORKDIR /home/hiventive

COPY *.py /home/hiventive/

ENTRYPOINT ["kopf", "run" , "-n", "kube-system", "/home/hiventive/controller.py"]
