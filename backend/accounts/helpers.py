""" Вспомогательные функции для моделей из Accounts. """

from django.contrib.auth.models import Group

from accounts.models import EmployeeRoles


def get_director_group() -> Group:
    """ Возвращает группу Директоров """
    return Group.objects.get_by_natural_key(EmployeeRoles.DIRECTOR.label)  # pylint: disable=no-member
