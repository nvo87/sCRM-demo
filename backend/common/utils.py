""" Common helper functions """
import re

from django.core.exceptions import ValidationError


def clean_phone_to_rus_format(phone: str) -> str:
    """ Оставляет только цифры и прибавляет +7 к главным 10 цифрам номера.

    :param phone: номер телефона в любом формате, с 8 или +7 в начале
    :raise ValidationError: если в номере недостаточно знаков
    """
    MIN_DIGITS_AMOUNT = 10  # 123-123-45-67
    MAX_DIGITS_AMOUNT = 11  # 8-123-123-45-67

    digit_regex = r'([0-9])'
    phone = ''.join(re.findall(digit_regex, phone))

    if not MIN_DIGITS_AMOUNT <= len(phone) <= MAX_DIGITS_AMOUNT:
        raise ValidationError(
            f'Номер должен быть больше {MIN_DIGITS_AMOUNT} и меньше {MAX_DIGITS_AMOUNT} знаков', params={'value': phone}
        )

    return f'+7{phone[-10:]}'
