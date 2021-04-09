from django.db import models

from core.models import EmployeeUser


class Employee(models.Model):
    first_name = models.CharField('Имя', max_length=64)
    last_name = models.CharField('Фамилия', max_length=64)
    third_name = models.CharField('Отчество', max_length=64, blank=True)
    account = models.OneToOneField(EmployeeUser, primary_key=True, related_name='profile', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def email(self):
        return self.account.email
