""" Валидаторы для наиболее частых случаев """

from django.core.exceptions import ValidationError


def validate_phone(value: str) -> None:
    """
     Проверка телефонного номера на адекватность.

    :param value:
    :return: None
    :raise ValidationError: В случае если мало знаков или не похож на русский.
    """
    PHONE_ALL_CHARS_LENGTH = 12
    RUS_CODE = '+7'

    if len(value) != PHONE_ALL_CHARS_LENGTH:
        raise ValidationError(
            f'Номер должен быть больше {PHONE_ALL_CHARS_LENGTH} знаков', params={'value': value}
        )

    if value[:2] != RUS_CODE:
        raise ValidationError(
            f'Номер должен начинаться с {RUS_CODE}', params={'value': value}
        )
