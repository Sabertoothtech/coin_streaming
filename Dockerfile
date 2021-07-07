FROM python:3

WORKDIR app

COPY . /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

CMD ["python","test1.py"]


