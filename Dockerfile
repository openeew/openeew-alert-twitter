FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python3", "sub_to_openeew_event.py"]
