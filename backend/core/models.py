# TODO Оставить данный файл только для работы с юзерами и переименовать в models/user.py
"""
    Описывает работу с пользователями CRM. Причина создания своей модели юзера - это аккаунты нескольких типов.
    Могут быть как аккаунты для игроков, так и для сотрудников. Вход в каждый аккаунт выполняется с разными полями
    (напр. клиенты - через телефон, сотрудники - через почту). У каждого типа аккаунта доступ к разным интерфейсам CRM.
    Для этого реализована одна центральная модель User. От нее наследуются прокси-модели для отдельного типа аккаунта.
    Логика разделения доступов и прав ложится на группы, к которым относится конкретный аккаунт.
"""
from typing import Optional

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.db import models
from django.utils import timezone

from common.utils import clean_phone_to_rus_format
from common.validators import validate_phone


class UserManager(BaseUserManager):
    """ Реализует методы для работы с базовой моделью User.
    Является суперклассом для менеджеров от более специфичных пользователей (сотрудник клуба или клиент).
    """

    def create_user(self, login: str, password: str, **extra_fields) -> 'User':
        """ Дает возможность создать пользователя в самом общем виде и с любыми полями, напрямую через поле login.
        Данный метод можно использовать для создания аккаунта разработчиков сотрудников CRM.

        :param login: уникальный идентификатор пользователя
        :param password: пароль
        :param extra_fields: доп. атрибуты пользователя, которые будут сохранены при создании
        :return: User
        """
        if not password:
            raise ValueError('Password is empty.')

        user = self.model(login=login.lower(), **extra_fields)
        user.set_password(raw_password=password)
        user.save(using=self._db)

        return user

    def create_superuser(self, login: str, password: str, **extra_fields) -> 'User':
        """
        Создает пользователя с правами superuser.

        :param login: уникальный идентификатор пользователя
        :param password: пароль
        :param extra_fields: доп. атрибуты пользователя, которые будут сохранены при создании
        :return: User
        """
        user = self.create_user(login, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Базовая модель пользователя. Может быть несколько типов аккаунтов, напр. сотрудники и клиенты.
    Здесь реализована базовая логика для всех типов аккаунтов. Для конкретного типа аккаунта наследуется своя
    proxy модель.
    """

    class Types(models.TextChoices):
        """ Типы пользователей - по ним создаются группы с разрешениями или определяется логика авторизации. """
        CLIENT = 'CLIENT', 'Клиент'
        EMPLOYEE = 'EMPLOYEE', 'Сотрудник клуба'

    login = models.CharField('Логин', max_length=150, unique=True, blank=True,
                             help_text='Ваш идентификатор, например, email или телефон, '
                                       'по которому вас зарегистрировали')
    phone = models.CharField('Номер телефона', max_length=12, unique=True, null=True, blank=True,
                             validators=[validate_phone], help_text='+79871234567')
    email = models.EmailField('Email', unique=True, null=True, blank=True, )
    is_staff = models.BooleanField('Технический Сотрудник сервиса', default=False,
                                   help_text='Определяет, может ли юзер иметь доступ в суперадминку.')
    is_active = models.BooleanField('Аккаунт активен', default=True,
                                    help_text='Отключает аккаунт вместо физического удаления из БД. '
                                              'Только Сотрудник сервиса может сделать вновь активным.')
    date_joined = models.DateTimeField('Дата создания аккаунта', default=timezone.now)

    # исп. именно имя USERNAME_FIELD (напр. не LOGIN_FIELD)
    # т.к. AbstractBaseUser использует его во многих своих методах.
    USERNAME_FIELD = 'login'

    DEFAULT_GROUP_NAME = None  # сопоставляет в какую группу попадает юзер при создании. Используется в дочерних классах

    objects = UserManager()

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def clean_fields(self, exclude=None):
        self.phone = clean_phone_to_rus_format(self.phone) if self.phone else None
        self.email = self.__class__.objects.normalize_email(self.email) if self.email else None

        return super().clean_fields(exclude=None)

    @property
    def default_group(self) -> Optional[Group]:
        """ Группа, к которой пользователь по умолчанию относится после создания. """
        try:
            return Group.objects.get(name=self.DEFAULT_GROUP_NAME)
        except Group.DoesNotExist:
            return None

    def add_to_default_group(self) -> None:
        group = self.default_group
        if not group:
            raise ValueError('Group for your User type is absent or model.DEFAULT_GROUP_NAME is empty.')
        group.user_set.add(self)


class UserWithTypeManager(UserManager):
    """ Менеджер для пользователей с аккаунтом определенного типа. В зависимости от модели, из которой вызывается
    менеджер, будет возвращена логика для этого типа аккаунта. """

    def get_queryset(self):
        return super().get_queryset().filter(groups=self.model().default_group)

    def create_superuser(self, login, password, **extra_fields):
        raise NotImplementedError(f'{self.model().DEFAULT_GROUP_NAME} User cannot create superusers. ')

    def _create_user_obj(self, **fields) -> User:
        """
        Возвращает объект User, готовый к сохранению.

        :param fields: передаются все поля из атрибутов USERNAME_FIELD и REQUIRED_FIELDS модели. Значение из
                        USERNAME_FIELD будет взято для поля login.
        """

        login = fields.get(self.model().USERNAME_FIELD, None)
        if not login:
            raise ValueError(f'You need to specify {self.model().USERNAME_FIELD} field value '
                             f'to create {self.model().DEFAULT_GROUP_NAME} User.')

        user = self.model(login=login)
        for field in self.model().REQUIRED_FIELDS:
            value = fields.get(field, None)
            if not value:
                raise ValueError(f'{field} field is required to create {self.model().DEFAULT_GROUP_NAME} User.')

            setattr(user, field, value)

        return user

    def create_user(self, password, **fields) -> 'User':  # pylint: disable=arguments-differ
        """
        Создает и сохраняет юзера для аккаунта определенного типа. В зависимости от модели юзера, в **fields передаются
        поля, которые необходимы данной модели. Поэтому в качестве обязательных параметров используется только password.

        :param password: пароль
        :param fields: значения полей из REQUIRED_FIELDS модели, плюс любые другие поля.
        :return: User
        """

        if not password:
            raise ValueError('Password is empty.')

        user = self._create_user_obj(**fields)
        user.set_password(raw_password=password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)

        user.add_to_default_group()

        return user


class EmployeeUser(User):
    """
    Аккаунты Сотрудников.
    """

    class Meta:
        proxy = True

    objects = UserWithTypeManager()

    DEFAULT_GROUP_NAME = User.Types.EMPLOYEE.label  # pylint: disable=no-member
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']


class ClientUser(User):
    """
    Аккаунты Клиентов.
    """

    class Meta:
        proxy = True

    objects = UserWithTypeManager()

    DEFAULT_GROUP_NAME = User.Types.CLIENT.label  # pylint: disable=no-member
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['phone']
