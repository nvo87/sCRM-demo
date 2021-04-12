import pytest

from django.test import TestCase

from clients.models import Client


@pytest.mark.skip(reason="Unresolved model scheme yet.")
class ClientTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client.objects.create(
            first_name='Владимир',
            last_name='Иванов',
            phone='9051231212',
            note='из Спартака'
        )

    def test_format_char_fields_with_none_values(self):
        """ Check if the field is None, there won't be an error """
        self.client.phone2 = None
        self.client.note = None
        self.client._format_char_fields()

        self.assertEqual(self.client.phone2, '')
        self.assertEqual(self.client.note, '')
