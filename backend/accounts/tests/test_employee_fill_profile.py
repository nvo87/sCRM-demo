from django.urls import reverse
from rest_framework import status

from accounts.models import Profile, User


def test_new_user_has_empty_profile(employee_user):
    """ Тестируем, что на только, что созданного юзера сразу есть запись в Profile """
    assert employee_user.profile
    assert employee_user.profile.first_name == ''


def test_employee_fill_profile(verified_employee_user, api_client):
    """ Тестируем, что юзер может изменить свой профиль и данные из модели User (phone, email) """
    user = verified_employee_user
    expected_phone = '+79031234567'

    url = reverse('accounts:user-detail', args=[user.id])
    data = {
        'user': user.id,
        'first_name': 'Виктор',
        'last_name': 'Тихонов',
        'third_name': 'Васильевич',
        'phone': expected_phone,
        'email': user.email
    }
    response = api_client.put(url, data)
    user = User.objects.get(email=user.email)

    assert response.status_code == status.HTTP_200_OK
    assert Profile.objects.get(user=user)
    assert user.phone == expected_phone
