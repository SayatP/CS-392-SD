FROM python:3.7
ADD ./requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
WORKDIR /code
ADD ./consumer.py /code/consumer.py
CMD python consumer.py
