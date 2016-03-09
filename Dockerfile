FROM python:latest

RUN mkdir -p /usr/src 
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
