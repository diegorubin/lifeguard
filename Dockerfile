FROM fedora:42


RUN dnf install -y python3 python3-pip python3-devel gcc mariadb-devel rust cargo

RUN mkdir /application
WORKDIR /application

COPY requirements.txt /application/requirements.txt
RUN pip3 install -r requirements.txt

COPY bot_handlers /application/bot_handlers
COPY validations /application/validations
COPY custom_settings.py /application/custom_settings.py
COPY lifeguard_settings.py /application/lifeguard_settings.py


CMD ["lifeguard"]
