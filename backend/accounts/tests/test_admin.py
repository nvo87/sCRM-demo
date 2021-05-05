import pytest
from django.urls import reverse

from conftest import PASSWORD, CLIENT, EMPLOYEE


def test_superuser_can_login_to_the_admin(django_client, superuser, employee_user) -> None:
    """ Superuser can view admin pages. """
    django_client.login(login=superuser.login, password=PASSWORD)
    url = reverse('admin:accounts_user_changelist')
    res = django_client.get(url)

    assert employee_user.email in str(res.content)


@pytest.mark.parametrize("user_type", [CLIENT, EMPLOYEE])
def test_custom_users_cant_login_to_the_admin(django_client, user_type, user) -> None:
    """ Custom user cant view the admin pages and their are redirected to the login page """
    _user = user(user_type)
    django_client.login(login=_user.login, password=PASSWORD)

    url = reverse('admin:accounts_user_changelist')
    res = django_client.get(url)

    login_url = reverse('admin:login')
    assert login_url in res.url
