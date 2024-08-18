import pytest
from cinemaTicket.models import Movie
from django.core.exceptions import ObjectDoesNotExist

url = "/api/movie/"

@pytest.mark.django_db
def test_can_create_cinema_movie(api_client_with_credentials, test_image):

    # Given an authorized user and new data
    movie_image = test_image

    movie_data = {"name": "Deadpool & Wolverine", 
                "description": "some movie description", 
                "poster_image": movie_image}

    # When post to /api/movie/ endpoint witch data

    response = api_client_with_credentials.post(path=url, data=movie_data, format="multipart")

    # Then the server respond with success data
    #print(response.data)

    response_data = response.data

    assert response_data["name"] == movie_data["name"]


@pytest.mark.django_db
def test_can_get_movie(api_client_with_credentials, given_cinema_movie):
    response = api_client_with_credentials.get(path=url)

    response_data = response.data

    db_query = Movie.objects.get(pk=response_data[0]["id"])

    assert db_query.id == response_data[0]["id"]


@pytest.mark.django_db
def test_can_update_movie(api_client_with_credentials, given_cinema_movie, test_image):

    movie_image = test_image

    movie_data = {"name": "wherever name", 
                "description": "some movie description", 
                "poster_image": movie_image}

    response = api_client_with_credentials.put(
        path=url + "1/", data=movie_data, format="multipart"
    )

    response_data = response.data

    assert response_data["name"] == movie_data["name"]


@pytest.mark.django_db
def test_can_delete_movie(api_client_with_credentials, given_cinema_movie):
    response = api_client_with_credentials.delete(path=url + "1/")

    try:
        db_query = Movie.objects.get(pk=1)
        pytest.fail(reason="the object exist!")

    except ObjectDoesNotExist:
        assert True