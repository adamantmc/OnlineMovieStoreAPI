from tests.common.utils import get_all_objects_pagination
from tests.authentication.utils import logged_in_client, create_random_user, login
from tests.movie_store.utils import *
from movie_store.logic.fees import FeeCalculator
import pytest
import uuid
import datetime

def test_get_rentals_no_auth(client):
    r = client.get(RENTALS_URL)
    assert r.status_code == 401


@pytest.mark.django_db
def test_get_rentals(logged_in_client):
    num_rentals = 10
    movies, genres = populate_db(num_movies=num_rentals*2, num_genres=5)
    rentals = create_rentals(movies, logged_in_client.user, num_rentals=num_rentals)

    r = logged_in_client.get(RENTALS_URL)

    assert r.status_code == 200
    returned_rentals = get_all_objects_pagination(logged_in_client, r)
    assert len(returned_rentals) == num_rentals

    for rental in returned_rentals:
        rental["movie"] = str(rental["movie"]) # uuid is returned as UUID obj, cast to str for equality
        assert any([rentals_equal(rental, r) for r in rentals])


@pytest.mark.django_db
def test_get_rental_no_auth(client):
    num_rentals = 10

    username, password, user_obj = create_random_user()
    movies, genres = populate_db(num_movies=num_rentals*2, num_genres=5)
    rentals = create_rentals(movies, user_obj, num_rentals=num_rentals)

    r = client.get(RENTAL_URL.format(uuid=rentals[0]["uuid"]))
    assert r.status_code == 401


@pytest.mark.django_db
def test_get_rental(logged_in_client):
    num_rentals = 1
    movies, genres = populate_db(num_movies=1, num_genres=1)
    rentals = create_rentals(movies, logged_in_client.user, num_rentals=num_rentals)

    r = logged_in_client.get(RENTAL_URL.format(uuid=rentals[0]["uuid"]))
    assert r.status_code == 200
    rental = r.data

    #TODO: really needed?
    rental["movie"] = str(rental["movie"])
    assert rentals_equal(rental, rentals[0])


@pytest.mark.django_db
def test_get_nonexistent_rental(logged_in_client):
    r = logged_in_client.get(RENTAL_URL.format(uuid=uuid.uuid4()))
    assert r.status_code == 404


@pytest.mark.django_db
def test_rental_ownership(client):
    # create rentals for user 1
    username, password, user_obj = create_random_user()
    login(client, username, password)
    movies, genres = populate_db(num_movies=5, num_genres=5)
    user1_rentals = create_rentals(movies, user_obj, num_rentals=5)

    # create and login with user 2
    username, password, user_obj = create_random_user()
    login(client, username, password)

    r = client.get(RENTALS_URL)
    assert r.data["count"] == 0

    r = client.get(RENTAL_URL.format(uuid=user1_rentals[0]["uuid"]))
    assert r.status_code == 403


@pytest.mark.django_db
def test_rent_movie_no_auth(client):
    movies, genres = populate_db(num_movies=1, num_genres=1)

    r = client.post(RENTALS_URL, {"movie": movies[0]["uuid"]})
    assert r.status_code == 401


@pytest.mark.django_db
def test_rent_movie(logged_in_client):
    movies, genres = populate_db(num_movies=1, num_genres=1)
    movie = movies[0]

    r = logged_in_client.post(RENTALS_URL, {"movie": movie["uuid"]})

    assert r.status_code == 201
    assert r.data["movie"] == movies[0]["uuid"]


@pytest.mark.django_db
def test_rent_movie_noneditable_fields(logged_in_client):
    movies, genres = populate_db(num_movies=1, num_genres=1)
    movie_uuid = movies[0]["uuid"]

    r = logged_in_client.post(RENTALS_URL, {"movie": movie_uuid, "fee": 1})
    assert r.status_code == 400
    r = logged_in_client.post(RENTALS_URL, {"movie": movie_uuid, "rental_date": datetime.datetime(2000, 1, 1)})
    assert r.status_code == 400
    r = logged_in_client.post(RENTALS_URL, {"movie": movie_uuid, "owner": 1})
    assert r.status_code == 400
    r = logged_in_client.post(RENTALS_URL, {"movie": movie_uuid, "return_date": datetime.datetime(2000, 1, 1)})
    assert r.status_code == 400
    r = logged_in_client.post(RENTALS_URL, {"movie": movie_uuid, "returned": True})
    assert r.status_code == 400


@pytest.mark.django_db
def test_rent_movie_wrong_uuid(logged_in_client):
    r = logged_in_client.post(RENTALS_URL, {"movie": str(uuid.uuid4())})

    # We would expect that using a uuid that points to a non-existent object would result in 404 and not 400.
    # However, in this case the uuid is part of the request data, and more specifically
    # it is the movie to be rented. Since no movie exists with that uuid, the request is
    # invalid, hence the 400.
    assert r.status_code == 400


@pytest.mark.django_db
def test_rent_movie_twice(logged_in_client):
    movies, genres = populate_db(num_movies=1, num_genres=1)
    movie = movies[0]

    r = logged_in_client.post(RENTALS_URL, {"movie": movie["uuid"]})

    assert r.status_code == 201
    assert r.data["movie"] == movies[0]["uuid"]

    r = logged_in_client.post(RENTALS_URL, {"movie": movie["uuid"]})
    assert r.status_code == 400


@pytest.mark.django_db
def test_two_users_rent_same_movie(client):
    movies, genres = populate_db(num_movies=5, num_genres=5)
    movie = movies[0]

    username1, password1, user_obj1 = create_random_user()
    login(client, username1, password1)
    r = client.post(RENTALS_URL, {"movie": movie["uuid"]})
    assert r.status_code == 201

    username2, password2, user_obj2 = create_random_user()
    login(client, username2, password2)
    r = client.post(RENTALS_URL, {"movie": movie["uuid"]})
    assert r.status_code == 201


@pytest.mark.django_db
def test_patch_rental_noneditable_fields(logged_in_client):
    movies, genres = populate_db(num_movies=2, num_genres=1)
    movie = movies[0]

    r = logged_in_client.post(RENTALS_URL, {"movie": movie["uuid"]})
    rental_uuid = r.data["uuid"]

    assert r.status_code == 201
    assert r.data["movie"] == movies[0]["uuid"]

    r = logged_in_client.patch(RENTAL_URL.format(uuid=rental_uuid), {"movie": movies[1]["uuid"]},
                               content_type='application/json')
    assert r.status_code == 400
    r = logged_in_client.patch(RENTAL_URL.format(uuid=rental_uuid), {"fee": 5},
                               content_type='application/json')
    assert r.status_code == 400
    r = logged_in_client.patch(RENTAL_URL.format(uuid=rental_uuid), {"rental_date": datetime.datetime.now()},
                               content_type='application/json')
    assert r.status_code == 400
    r = logged_in_client.patch(RENTAL_URL.format(uuid=rental_uuid), {"return_date": datetime.datetime.now()},
                               content_type='application/json')
    assert r.status_code == 400


@pytest.mark.django_db
def test_patch_rental_no_data_no_change(logged_in_client):
    movies, genres = populate_db(num_movies=2, num_genres=1)
    movie = movies[0]

    r1 = logged_in_client.post(RENTALS_URL, {"movie": movie["uuid"]})
    rental_uuid = r1.data["uuid"]

    assert r1.status_code == 201
    assert r1.data["movie"] == movies[0]["uuid"]

    r2 = logged_in_client.patch(RENTAL_URL.format(uuid=rental_uuid), data={}, content_type='application/json')
    assert r2.status_code == 200
    assert dicts_equal(r1.data, r2.data)


@pytest.mark.django_db
def test_return_movie_no_auth(client):
    username, password, user_obj = create_random_user()
    movies, genres = populate_db(num_movies=5, num_genres=5)
    rentals = create_rentals(movies, user_obj, num_rentals=5)

    r = client.patch(RENTAL_URL.format(uuid=rentals[0]["uuid"]), {"returned": True}, content_type='application/json')
    assert r.status_code == 401


@pytest.mark.django_db
def test_return_movie_nonexistent_rental(logged_in_client):
    movies, genres = populate_db(num_movies=5, num_genres=5)
    rentals = create_rentals(movies, logged_in_client.user, num_rentals=5)

    r = logged_in_client.patch(RENTAL_URL.format(uuid=uuid.uuid4()), {"returned": True}, content_type='application/json')
    assert r.status_code == 404


@pytest.mark.django_db
def test_return_movie(logged_in_client):
    movies, genres = populate_db(num_movies=5, num_genres=5)
    rentals = create_rentals(movies, logged_in_client.user, num_rentals=5)

    r = logged_in_client.patch(RENTAL_URL.format(uuid=rentals[0]["uuid"]), {"returned": True}, content_type='application/json')
    assert r.status_code == 200

    assert "return_date" in r.data
    assert "fee" in r.data

    # assert that the fee is equal as the fee charged between two aslmost-identical timestamps
    t1 = datetime.datetime.now(datetime.timezone.utc)
    t2 = datetime.datetime.now(datetime.timezone.utc)

    fee_calculator = FeeCalculator(t1, t2)
    assert r.data["fee"] == fee_calculator.calculate_fee()


@pytest.mark.django_db
def test_return_movie_twice(logged_in_client):
    movies, genres = populate_db(num_movies=5, num_genres=5)
    rentals = create_rentals(movies, logged_in_client.user, num_rentals=5)

    r = logged_in_client.patch(RENTAL_URL.format(uuid=rentals[0]["uuid"]), {"returned": True}, content_type='application/json')
    assert r.status_code == 200

    r = logged_in_client.patch(RENTAL_URL.format(uuid=rentals[0]["uuid"]), {"returned": True}, content_type='application/json')
    assert r.status_code == 400


@pytest.mark.django_db
def test_return_another_user_move(client):
    # user1
    _, _, user_obj = create_random_user()
    movies, genres = populate_db(num_movies=5, num_genres=5)
    rentals = create_rentals(movies, user_obj, num_rentals=5)

    # user2
    username, password, user_obj = create_random_user()

    login(client, username, password)
    r = client.patch(RENTAL_URL.format(uuid=rentals[0]["uuid"]), {"returned": True}, content_type='application/json')
    assert r.status_code == 403


@pytest.mark.django_db
def test_consecutive_rent_return(logged_in_client):
    movies, genres = populate_db(num_movies=1, num_genres=1)
    movie = movies[0]

    for i in range(5):
        r = logged_in_client.post(RENTALS_URL, {"movie": movie["uuid"]})

        assert r.status_code == 201
        assert r.data["movie"] == movies[0]["uuid"]

        rental_uuid = r.data["uuid"]

        r = logged_in_client.patch(RENTAL_URL.format(uuid=rental_uuid), {"returned": True}, content_type='application/json')
        assert r.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "diff, result",
    [
        ({"days": 0, "seconds": 1}, 1),
        ({"days": 1, "seconds": 1}, 2),
        ({"days": 2, "seconds": 1}, 3),
        ({"days": 3, "seconds": 1}, 3.5),
        ({"days": 4, "seconds": 1}, 4),
        ({"days": 5, "seconds": 1}, 4.5)
    ]
)
def test_fee_calculation_standard(logged_in_client, diff, result):
    username, password, user_obj = create_random_user()
    movies, genres = populate_db(num_movies=1, num_genres=5)
    rentals = create_rentals(movies, logged_in_client.user, num_rentals=1)

    rental_uuid = rentals[0]["uuid"]
    rental_obj = Rental.objects.get(uuid=rental_uuid)

    rental_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(**diff)
    rental_obj.rental_date = rental_date
    rental_obj.save()

    r = logged_in_client.patch(RENTAL_URL.format(uuid=rental_uuid), {"returned": True}, content_type='application/json')
    fee = r.data["fee"]

    assert fee == result


