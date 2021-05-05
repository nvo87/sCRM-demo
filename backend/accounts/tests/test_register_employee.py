from unittest.mock import patch

from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from conftest import PASSWORD


@patch("allauth.account.utils.send_email_confirmation")
def test_email_send_after_correct_signup(mock_send_email, api_client, enable_account_email_verification):
    """ Убедиться, что срабатывает метод отправки письма со ссылкой для верификации """

    url = reverse('accounts:employee-register')
    data = {
        'email': 'employee-test-reg@test.ru',
        'password1': PASSWORD,
        'password2': PASSWORD
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert mock_send_email.call_count


def test_activate_user_with_correct_link(employee_user, django_client, enable_account_email_verification):
    """ Убедиться, что аккаунт юзера активируется при заходе по ссылке с ключом """

    email_address = EmailAddress.objects.create(user=employee_user,
                                                email=employee_user.email,
                                                verified=False, primary=True)

    confirmation = EmailConfirmationHMAC(email_address)
    key = confirmation.key

    url = reverse('account_confirm_email', args=[key])
    data = {'key': key}

    response = django_client.get(url, data)

    email_address = EmailAddress.objects.get(email=employee_user.email)

    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL
    assert email_address.verified


def test_cannot_activate_with_invalid_link(employee_user, django_client, enable_account_email_verification):
    """ Проверяем, что юзер не может активировать аккаунт по неверной ссылке """

    EmailAddress.objects.create(
        user=employee_user, email=employee_user.email, verified=False, primary=True
    )
    key = 'invalid_key'
    url = reverse('account_confirm_email', args=[key])
    data = {'key': key}

    response = django_client.post(url, data)

    email_address = EmailAddress.objects.get(user=employee_user)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert not email_address.verified


def test_verified_employee_has_jwt_after_login(verified_employee_user, api_client):
    """ Проверяем, что сотруднику выдается jwt после логина """

    url = reverse('accounts:employee-login')
    data = {
        'email': verified_employee_user.email,
        'password': PASSWORD
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert 'key' in response.json()


def test_not_verified_employee_cannot_login(employee_user, api_client):
    """ Проверка, что сотрудник не проходивший верификацию не может войти. """

    url = reverse('accounts:employee-login')
    data = {
        'email': employee_user.email,
        'password': PASSWORD
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Employee user verified with email was not found' in str(response.content)
