FROM python:3

WORKDIR /opt/

RUN pip install --upgrade pip

COPY . .

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
