"""  Клубом может быть спорт.секция, команда, школа или клуб.
"""
from typing import Iterable

from django.db import models

from accounts.helpers import get_director_group
from accounts.models import User, Group


class Club(models.Model):
    """ Центральная модель, создающая связь между другими ключевыми моделями. """
    title = models.CharField('Название клуба', max_length=256)
    logo = models.ImageField('Логотип клуба', upload_to='images/clients/', default=None, blank=True, null=True)

    def clean(self, *args, **kwargs):
        self.title = self.title.title()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Клуб"
        verbose_name_plural = "Клубы"

    @property
    def directors(self) -> Iterable[User]:
        """ Возвращает список юзеров с группой Директор по данному клубу """
        return (User.objects
                .prefetch_related('membership__group', 'membership__club')
                .filter(membership__group=get_director_group(), membership__club=self))

    def add_user_group(self, user: User, group: Group) -> None:
        """ Добавляет юзера в группу, если он там еще не был """
        Membership.objects.get_or_create(club=self, user=user, group=group)


class Membership(models.Model):
    """ Определяет в каких клубах какую роль выполняет каждый юзер. """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='membership')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, related_name='membership')

    class Meta:
        db_table = 'clubs_user_groups'
        unique_together = ('group', 'user', 'club')
