FROM python:3.8-slim-buster

ADD requestPython.py /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "./requestPython.py"]