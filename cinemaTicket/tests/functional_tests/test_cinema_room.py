import pytest
from cinemaTicket.models import CinemaRoom
from django.core.exceptions import ObjectDoesNotExist

url = '/api/cinema-room/'

@pytest.mark.django_db
def test_can_create_cinema_room(api_client_with_credentials):
    # given an endpoint and a authorized user in database
  
  
    # when the user post some data in the end point 'api/cinema_room'
  
    data = {
        "name":"B1",
        "capacity":100
    }

    response = api_client_with_credentials.post(path=url, data=data, format='json')
    # then get the cinema_room data    
    response_data = response.data


    assert response_data["name"] == data["name"]


@pytest.mark.django_db
def test_can_get_cinema_room(api_client, given_cinema_rooms):

    response = api_client.get(path=url)

    response_data = response.data

    db_query = CinemaRoom.objects.get(pk=response_data[0]['id'])

    
    assert db_query.name == response_data[0]['name']


@pytest.mark.django_db
def test_can_update_cinema_room(api_client_with_credentials, given_cinema_rooms):
    
    response = api_client_with_credentials.patch(path=url + '1/', data={"capacity":120}, format='json')

    response_data = response.data

    db_query = CinemaRoom.objects.get(pk=response_data['id'])

    assert db_query.capacity == response_data['capacity']


@pytest.mark.django_db
def test_can_delete_cinema_room(api_client_with_credentials, given_cinema_rooms):
    
    response = api_client_with_credentials.delete(path=url + '1/')

    try:
        db_query = CinemaRoom.objects.get(pk=1)
        pytest.fail(reason="the object exist!")

    except ObjectDoesNotExist:
        assert True

    
