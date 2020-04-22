# Author:  Meryll Dindin
# Date:    11 April 2020
# Project: Funnel

FROM python:3.7-slim

MAINTAINER Meryll Dindin "meryll@calaster.com"

RUN mkdir /app
VOLUME /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install gunicorn
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 5000

CMD [ "gunicorn", "-w 3", "-b 0.0.0.0:5000", "--worker-class=gthread", "worker:app" ]