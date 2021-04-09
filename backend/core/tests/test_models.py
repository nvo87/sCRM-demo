from django.contrib.auth import authenticate
from django.test import TestCase

from core.models import EmployeeUser, User, ClientUser


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser(
            login='s_admin',
            password='123qweQWE',
        )

        self.staff_user = User.objects.create_user(
            login='staff_1',
            password='123qweQWE',
            is_staff=True,
        )

        self.employee = EmployeeUser.objects.create_user(
            email='employee_test@test.ru',
            password='123qweQWE'
        )

        self.client = ClientUser.objects.create_user(
            phone='+79051234567',
            password='123qweQWE'
        )

    def test_is_superuser(self) -> None:
        self.assertEqual(self.superuser.is_staff, True)
        self.assertEqual(self.superuser.is_superuser, True)

    def test_is_staff_user(self) -> None:
        self.assertEqual(self.staff_user.is_staff, True)

    def test_employee_can_authenticate(self) -> None:
        authenticate(self.employee)

        self.assertEqual(self.employee.is_authenticated, True)

    def test_employee_in_default_group(self):
        self.assertTrue(self.employee.groups.get(name=self.employee.DEFAULT_GROUP_NAME))

    def test_employee_get_queryset_filters_by_default_group(self):
        employees = EmployeeUser.objects.all()

        self.assertEqual(employees.count(), 1)
        self.assertEqual(employees.first().email, 'employee_test@test.ru')

    def test_create_employee_without_email_raises_error(self):
        """ Employee can't be created without email. """
        with self.assertRaises(ValueError):
            EmployeeUser.objects.create_user(
                phone='+79091234567',
                password='123qweQWE'
            )

    def test_create_employee_only_with_login_raises_error(self):
        """ It's not enough to create Employee only by login. """
        with self.assertRaises(ValueError):
            EmployeeUser.objects.create_user(
                login='user123',
                password='123qweQWE'
            )

    def test_employee_cant_create_staff(self):
        employee2 = EmployeeUser.objects.create_user(
            email='employee2_test@test.ru',
            password='123qweQWE',
            is_staff=True
        )
        self.assertEqual(employee2.is_staff, False)

    def test_employee_manager_cant_create_superuser(self):
        with self.assertRaises(NotImplementedError):
            EmployeeUser.objects.create_superuser(
                login='user123',
                password='123qweQWE'
            )
