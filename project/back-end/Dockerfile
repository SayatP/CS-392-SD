FROM python:3.7
ADD ./requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
WORKDIR /code
ADD ./app.py /code/app.py
CMD python app.py
