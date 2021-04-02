from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from core.models import EmployeeUser


class AdminTests(TestCase):

    def setUp(self) -> None:
        self.django_client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            login='nvo87',
            password='12345asdASD'
        )
        self.django_client.force_login(self.admin_user)

        self.user = EmployeeUser.objects.create_user(
            email='test1@yandex.ru',
            password='12345asdASD',
        )

    def test_users_listed(self):
        url = reverse('admin:core_user_changelist')
        res = self.django_client.get(url)

        self.assertContains(res, self.user.email)
