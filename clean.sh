rm db.sqlite3

rm "./movie_store/migrations/0*.py"
rm "./authentication/migrations/0*.py"

rm -rf ./movie_store/migrations/__pycache__/
rm -rf ./authentication/migrations/__pycache__/

python3.8 manage.py makemigrations
python3.8 manage.py migrate
python3.8 populate_db.py
