import pytest


@pytest.mark.django_db
def test_can_get_success_response(
    api_client_with_credentials, given_cinema_movie, test_image
):

    movie_image = test_image

    movie_data = {
        "name": "Deadpool & Wolverine",
        "description": "some movie description",
        "poster_image": movie_image,
    }

    request = api_client_with_credentials.put(
        path="/api/movie/1/", data=movie_data, format="multipart"
    )
    assert request.status_code == 200


@pytest.mark.django_db
def test_can_reject_malformed_request_body(
    api_client_with_credentials, given_cinema_movie
):

    dirty_data = {"bad_data": 2, "pikachu": "some description"}

    request = api_client_with_credentials.put(
        path="/api/movie/1/", data=dirty_data, format="multipart"
    )

    assert request.status_code == 400


@pytest.mark.django_db
def test_can_reject_unauthorized_request(api_client, given_cinema_movie, test_image):

    movie_image = test_image

    movie_data = {
        "name": "Deadpool & Wolverine",
        "description": "some movie description",
        "poster_image": movie_image,
    }

    request = api_client.put(path="/api/movie/1/", data=movie_data, format="multipart")

    assert request.status_code == 403
