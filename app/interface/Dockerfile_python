FROM python:3.8

# create destination directory
RUN mkdir -p /usr/src
WORKDIR /usr/src

# copy files
COPY requirements.txt ./
COPY pluie.png ./
COPY soleil.png ./  

RUN pip3 install -r requirements.txt