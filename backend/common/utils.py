""" Common helper functions """


def format_phone_to_rus_code(phone: str) -> str:
    """ Add +7 to main 10 numbers of phone
    >>> format_phone_to_rus_code('81234567890')
    '+71234567890'
    >>> format_phone_to_rus_code('1234567890')
    '+71234567890'
    >>> format_phone_to_rus_code('')
    ''
    """
    if not phone:
        return ''
    return f'+7{phone[-10:]}'
