FROM python:3

ADD requirements.txt /code/requirements.txt

WORKDIR /code/

RUN pip install -r requirements.txt
