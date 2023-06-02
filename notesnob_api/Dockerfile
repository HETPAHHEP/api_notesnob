FROM python:3.11.3

RUN mkdir /code

COPY requirements.txt /code
RUN pip3 install -r /code/requirements.txt --no-cache-dir

COPY . /code
WORKDIR /code

CMD ["gunicorn", "notesnob_api.wsgi:application", "--bind", "0:8000" ]