""" Набор основных моделей для app Clients. """

from django.db import models
from autoslug import AutoSlugField

from common.utils import clean_phone_to_rus_format
from core.models import ClientUser


class Club(models.Model):
    """ Клубом может быть спорт.секция, команда, школа или клуб.
    К клубу относятся сотрудники (Employee), локации (Location) и мероприятия (Event).
    Игрок попавший хотя бы на одно мероприятие клуба - становится Клиентом (Client). """
    title = models.CharField('Название клуба', max_length=256)
    logo = models.ImageField('Логотип клуба', )

    def save(self, *args, **kwargs):
        self.title = self.title.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Клуб"
        verbose_name_plural = "Клубы"


class Location(models.Model):
    """ Локацией может быть каток, зал и т.д. - любое место для проведения мероприятий (тренировок). """
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    name = models.CharField('Название локации', max_length=64, help_text='Ваша арена, стадион, зал, каток.')
    description = models.CharField('Краткое описание', max_length=1024)
    slug = AutoSlugField(populate_from='name', unique_with=['club', ])

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class Client(models.Model):
    """ Клиент - это игрок, хотя бы раз попавший на мероприятие клуба. Он может чистлится в разных клубах.
    В каждом клубе игрок может показываться в разных локациях. """
    first_name = models.CharField('Имя', max_length=64)
    last_name = models.CharField('Фамилия', max_length=64)
    third_name = models.CharField('Отчество', max_length=64, blank=True)
    phone2 = models.CharField('Телефон для месенджеров (whatsapp и т.д.)', max_length=12, unique=True, blank=True,
                              help_text='+79871234567', db_index=True)
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    photo = models.ImageField('Фото', blank=True, null=True, upload_to='images/clients/', default=None)
    note = models.CharField('Заметка', max_length=256, blank=True,
                            help_text='Небольшая пометка по игроку в одно-два слова')
    locations = models.ManyToManyField(Location, verbose_name='Доступен в локациях', blank=True,
                                       help_text='Какие катки хоть раз посетил.')
    account = models.OneToOneField(ClientUser, primary_key=True, related_name='profile', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def phone(self):
        return self.account.phone

    def _format_char_fields(self) -> None:
        """ Преобразовывает строковые поля к нужному виду. """
        self.first_name = self.first_name.title() if self.first_name else None
        self.last_name = self.last_name.title() if self.last_name else None
        self.third_name = self.third_name.title() if self.third_name else None
        self.note = str(self.note).lower() if self.note else None
        self.phone2 = clean_phone_to_rus_format(self.phone2) if self.phone2 else None

    def save(self, *args, **kwargs):
        self._format_char_fields()
        super().save(*args, **kwargs)
