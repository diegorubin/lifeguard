FROM python:3.7-buster

RUN apt-get update

RUN mkdir /application
WORKDIR /application

COPY requirements.txt /application/requirements.txt
RUN pip3 install -r requirements.txt

COPY validations /application/validations
COPY lifeguard_settings.py /application/lifeguard_settings.py


CMD ["lifeguard"]
