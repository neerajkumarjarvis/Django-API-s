FROM python:3.8

WORKDIR /panna
COPY requirements.txt /panna
RUN pip install -r requirements.txt
COPY . /panna/