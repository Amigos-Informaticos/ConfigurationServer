FROM python:3.9.5-alpine3.13

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

RUN pip3 install gunicorn

CMD ["gunicorn", "-b", "0.0.0.0:42100", "app:run_app"]