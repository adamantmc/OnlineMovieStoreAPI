FROM python:3.8-slim-buster

COPY ./ /src/

RUN pip install -r ./src/requirements.txt

WORKDIR ./src/

CMD gunicorn OnlineMovieStore.wsgi -b 0.0.0.0:8000