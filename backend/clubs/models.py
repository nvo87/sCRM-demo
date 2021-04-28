"""  Клубом может быть спорт.секция, команда, школа или клуб.
"""

from django.db import models

from accounts.models import ClientUser, EmployeeUser


class Club(models.Model):
    """ Центральная модель, создающая связь между другими ключевыми моделями. """
    clients = models.ManyToManyField(ClientUser, verbose_name='Клиенты', related_name='play_in_clubs')
    employees = models.ManyToManyField(EmployeeUser, verbose_name='Сотрудники', related_name='work_in_clubs')

    title = models.CharField('Название клуба', max_length=256)
    logo = models.ImageField('Логотип клуба', upload_to='images/clients/', default=None, blank=True, null=True)

    def clean(self, *args, **kwargs):
        self.title = self.title.title()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Клуб"
        verbose_name_plural = "Клубы"
