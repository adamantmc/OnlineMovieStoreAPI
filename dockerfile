FROM python:3.8-slim-buster

COPY ./ /src/

RUN pip install -r ./src/requirements.txt

WORKDIR ./src/

RUN rm db.sqlite3

RUN python3.8 manage.py migrate

CMD gunicorn OnlineMovieStore.wsgi -b 0.0.0.0:8000