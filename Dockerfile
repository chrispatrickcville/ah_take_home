FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python python3-pip python3-dev git

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip3 install -r /usr/src/app/requirements.txt

CMD [ "./run.sh" ]