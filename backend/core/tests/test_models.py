import pytest
from django.contrib.auth import authenticate

from .conftest import SUPERUSER, STAFF, CLIENT, EMPLOYEE, PASSWORD
from ..models import EmployeeUser, User


def test_is_superuser(superuser) -> None:
    """ Check CustomManager's create_superuser method. """
    assert superuser.is_staff
    assert superuser.is_superuser


def test_is_staff_user(staff_user) -> None:
    assert staff_user.is_staff


@pytest.mark.parametrize("user_type", [SUPERUSER, STAFF, CLIENT, EMPLOYEE])
def test_user_can_authenticate(user_type, user) -> None:
    """ All user types can be authenticated. """
    _user = user(user_type)
    authenticate(_user)
    assert _user.is_authenticated


@pytest.mark.parametrize("user_type", [CLIENT, EMPLOYEE])
def test_user_is_in_default_group(user_type, user) -> None:
    """ Specific type user is in their DEFAULT_GROUP. """
    _user = user(user_type)
    assert _user.groups.get(name=_user.DEFAULT_GROUP_NAME)


@pytest.mark.django_db
def test_employee_get_queryset_filters_by_default_group(employee_user, client_user, staff_user) -> None:
    """ Proxy models is filtering their user type correctly. """
    users = User.objects.all()
    employees = EmployeeUser.objects.all()

    assert users.count() == 3
    assert employees.count() == 1
    assert employees.first().email == 'employee_test@test.ru'


@pytest.mark.parametrize("credentials", [{'phone': '+79091234567'}, {'login': 'user123'}])
def test_create_employee_without_email_raises_error(credentials) -> None:
    """ Employee can't be created without email. """
    with pytest.raises(ValueError) as field_exception:
        EmployeeUser.objects.create_user(password=PASSWORD, **credentials)
    assert 'You need to specify email field value ' in str(field_exception.value)


@pytest.mark.django_db
def test_employee_cant_create_staff() -> None:
    employee2 = EmployeeUser.objects.create_user(
        email='employee2_test@test.ru',
        password=PASSWORD,
        is_staff=True
    )
    assert not employee2.is_staff


def test_employee_manager_cant_create_superuser() -> None:
    with pytest.raises(NotImplementedError):
        EmployeeUser.objects.create_superuser(
            login='user123',
            password=PASSWORD
        )
