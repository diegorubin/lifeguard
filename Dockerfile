FROM python:3.7-buster

RUN curl -LsS -O https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN bash mariadb_repo_setup --mariadb-server-version=10.9

RUN apt-get update -y
RUN apt-get upgrade -y

RUN mkdir /application
WORKDIR /application

COPY requirements.txt /application/requirements.txt
RUN pip3 install -r requirements.txt

COPY bot_handlers /application/bot_handlers
COPY validations /application/validations
COPY custom_settings.py /application/custom_settings.py
COPY lifeguard_settings.py /application/lifeguard_settings.py


CMD ["lifeguard"]
