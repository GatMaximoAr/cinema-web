import pytest


@pytest.mark.django_db
def test_can_get_success_response(api_client_with_credentials, test_image):

    movie_image = test_image

    movie_data = {
        "name": "Deadpool & Wolverine",
        "description": "some movie description",
        "poster_image": movie_image,
    }

    request = api_client_with_credentials.post(
        path="/api/movie/", data=movie_data, format="multipart"
    )
    assert request.status_code == 200 or request.status_code == 201


@pytest.mark.django_db
def test_can_reject_malformed_request_body(api_client_with_credentials):

    dirty_data = {"bad_data": 2, "pikachu": "some description"}

    request = api_client_with_credentials.post(
        path="/api/movie/", data=dirty_data, format="json"
    )

    assert request.status_code == 400


@pytest.mark.django_db
def test_can_reject_unauthorized_request(api_client, test_image):

    movie_image = test_image

    movie_data = {
        "name": "Deadpool & Wolverine",
        "description": "some movie description",
        "poster_image": movie_image,
    }

    request = api_client.post(path="/api/movie/", data=movie_data, format="multipart")

    assert request.status_code == 403
