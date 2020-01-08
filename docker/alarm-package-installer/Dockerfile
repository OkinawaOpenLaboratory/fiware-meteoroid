FROM alpine:latest

RUN wget https://github.com/apache/openwhisk-cli/releases/download/1.0.0/OpenWhisk_CLI-1.0.0-linux-amd64.tgz
RUN tar zxvf OpenWhisk_CLI-1.0.0-linux-amd64.tgz -C /usr/local/bin/
RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
    bash git zip nodejs nodejs-npm
RUN mkdir /lib64
RUN ln -s /lib/libc.musl-x86_64.so.1 /lib64/ld-linux-x86-64.so.2
RUN git clone https://github.com/apache/openwhisk-package-alarms.git && cd openwhisk-package-alarms/
