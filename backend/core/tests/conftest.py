import pytest
from django.test import Client as DjangoClient

from core.models import User, EmployeeUser, ClientUser

SUPERUSER = 0
STAFF = 1
EMPLOYEE = 2
CLIENT = 3

PASSWORD = '123qweQWE'


@pytest.fixture(autouse=True)
def enable_db_access(db):  # pylint: disable=unused-argument
    pass


@pytest.fixture
def user(superuser, staff_user, employee_user, client_user):
    def wrapper(user_type):
        user_type_mapping = {
            SUPERUSER: superuser,
            STAFF: staff_user,
            EMPLOYEE: employee_user,
            CLIENT: client_user,
        }
        return user_type_mapping[user_type]

    return wrapper


@pytest.fixture
def superuser() -> User:
    return User.objects.create_superuser(
        login='s_admin',
        password=PASSWORD,
    )


@pytest.fixture()
def staff_user() -> User:
    return User.objects.create_user(
        login='staff_1',
        password=PASSWORD,
        is_staff=True,
    )


@pytest.fixture
def employee_user() -> EmployeeUser:
    return EmployeeUser.objects.create_user(
        email='employee_test@test.ru',
        password=PASSWORD
    )


@pytest.fixture
def client_user() -> ClientUser:
    return ClientUser.objects.create_user(
        phone='+79051234567',
        password=PASSWORD
    )


@pytest.fixture
def django_client() -> DjangoClient:
    return DjangoClient()
