# Online Movie Store API

API for an Online Movie Store made with `django` and `django-rest-framwork`.

## Dependencies
The API was built with `python3.8` and the dependencies in the `requirements.txt` folder.

## Running
The API can be run by starting the django server as such:
```
python3.8 manage.py runserver
```

## Adding users
The `add_user.py` file adds users to the database:
```
python3.8 add_user.py <username> <password>
```

## Testing
The tests can be found in the `tests` folder and run with:
```
pytest tests/
```

## Docker
The `dockerfile` file can be built into a docker image by going into the `api` directory and running:

```
docker build -f ../devops/dockerfile -t online_movie_store_api:latest .
```

A container can then start by running:

```
docker run --detach -p 8000:8000 online_movie_store_api:latest
```

The `-p 8000:8000` argument maps the container's port 8000 to the hosts's port 8000.

Building the dockerfile creates a new database and applies the migrations and also 
adds a default user with the following credentials:

`username`: user
`password`: user
