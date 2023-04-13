FROM python:3.7
ADD ./requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
WORKDIR /code
ADD ./app.py /code/app.py
CMD gunicorn --bind 0.0.0.0:5000 --workers 5 --worker-connections 1000 --worker-class 'gevent' --timeout 120 app:app
