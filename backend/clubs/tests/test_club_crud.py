from django.urls import reverse
from rest_framework import status

from clubs.models import Club
from conftest import PASSWORD


def test_user_create_club(verified_employee_user, api_client):
    """ Проверяем, что юзер создает клуб и становится его директором. """
    expected_title = 'Spartak'
    api_client.login(email=verified_employee_user.email, password=PASSWORD)

    url = reverse('clubs:club-list')
    data = {
        'title': expected_title,
        'logo': ''
    }

    resp = api_client.post(url, data)
    assert resp.status_code == status.HTTP_201_CREATED

    resp_data = resp.json()

    club = Club.objects.filter(id=resp_data['id']).first()
    assert club
    assert verified_employee_user in club.directors
