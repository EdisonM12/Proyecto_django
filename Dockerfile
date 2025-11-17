FROM ubuntu:latest
LABEL authors="Edison"

ENTRYPOINT ["top", "-b"]