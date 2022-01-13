FROM python:3.9.5-alpine3.13

WORKDIR /app

COPY . /app

RUN pip --no-cache-dir install -r requirements.txt

RUN pip install gunicorn

CMD ["gunicorn", "-b", "0.0.0.0:42100", "--certfile", "cert.pem", "--ca-certs", "chain.pem", "--keyfile", "privkey.pem", "--workers", "2", "app:app"]
