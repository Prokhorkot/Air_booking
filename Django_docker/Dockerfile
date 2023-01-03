# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /flask-docker

COPY requirements.txt /flask-docker/requirements.txt
RUN pip3 install -r requirements.txt

COPY .env /flask-docker/.env
COPY models.py /flask-docker/models.py
COPY session.py /flask-docker/session.py
COPY app.py /flask-docker/app.py
COPY templates /flask-docker/templates
COPY static /flask-docker/static

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]