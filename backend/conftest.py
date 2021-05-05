import pytest
from allauth.account.models import EmailAddress
from django.test import Client as DjangoClient
from rest_framework.test import APIClient

from accounts.models import User, EmployeeUser, ClientUser

SUPERUSER = 0
STAFF = 1
EMPLOYEE = 2
CLIENT = 3

PASSWORD = '123qweQWE'


@pytest.fixture(autouse=True)
def enable_db_access(db):  # pylint: disable=unused-argument
    pass


@pytest.fixture()
def disable_account_email_verification(settings):
    settings.ACCOUNT_EMAIL_VERIFICATION = 'none'


@pytest.fixture()
def enable_account_email_verification(settings):
    settings.ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    settings.ACCOUNT_CONFIRM_EMAIL_ON_GET = True
    settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'api/v1/employee/login'


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
def verified_employee_user() -> EmployeeUser:
    user = EmployeeUser.objects.create_user(
        email='employee_test_verified@test.ru',
        password=PASSWORD
    )
    EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
    return user


@pytest.fixture
def client_user() -> ClientUser:
    return ClientUser.objects.create_user(
        phone='+79051234567',
        password=PASSWORD
    )


@pytest.fixture
def django_client() -> DjangoClient:
    return DjangoClient()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
