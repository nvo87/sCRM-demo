import pytest
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from .conftest import SUPERUSER, STAFF, CLIENT, EMPLOYEE, PASSWORD
from ..models import EmployeeUser, User, EmployeeRoles


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


@pytest.mark.parametrize("raw_phone,clean_phone", [
    ('+71234567890', '+71234567890'),
    ('1234567890', '+71234567890'),
    ('81234567890', '+71234567890'),
    ('8-(123)-456-78-90', '+71234567890'),
    ('+7-(123)-456-78-90', '+71234567890'),
    ('', None),
    (None, None),
])
def test_clean_phone_field(raw_phone, clean_phone, client_user) -> None:
    client_user.phone = raw_phone
    client_user.clean_fields()
    client_user.save()
    assert client_user.phone == clean_phone


@pytest.mark.parametrize("bad_phone", ['+712345678901', '123456789', '8-(123)-456-78-'])
def test_clean_phone_field_raises_error(bad_phone, client_user) -> None:
    client_user.phone = bad_phone
    with pytest.raises(ValidationError):
        client_user.clean_fields()


def test_groups_from_employee_roles_exists():
    """ Проверяем, что были созданы все группы для ролей Сотрудников. """
    for role in EmployeeRoles:
        assert Group.objects.get(name=role.label)
