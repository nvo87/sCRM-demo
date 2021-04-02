from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.db import models
from django.utils import timezone

from common.utils import format_phone_to_rus_code


class UserManager(BaseUserManager):

    def create_user(self, login, password, **extra_fields):
        """ Creates and saves a new user """
        if not password:
            raise ValueError('Password is empty.')

        user = self.model(login=login.lower(), **extra_fields)
        user.set_password(raw_password=password)
        user.save(using=self._db)

        return user

    def create_superuser(self, login, password, **extra_fields):
        user = self.create_user(login, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    class Types(models.TextChoices):
        CLIENT = 'CLIENT', 'Клиент'
        EMPLOYEE = 'EMPLOYEE', 'Сотрудник клуба'

    login = models.CharField('Логин', max_length=150, unique=True, blank=True,
                             help_text='Ваш идентификатор, например, email или телефон, '
                                       'по которому вас зарегистрировали')
    phone = models.CharField('Номер телефона', max_length=12, unique=True, null=True, blank=True,
                             help_text='+79871234567')
    email = models.EmailField('Email', unique=True, null=True, blank=True, )
    is_staff = models.BooleanField('Технический Сотрудник сервиса', default=False,
                                   help_text='Определяет, может ли юзер иметь доступ в суперадминку.')
    is_active = models.BooleanField('Аккаунт активен', default=True,
                                    help_text='Отключает аккаунт вместо физического удаления из БД. '
                                              'Только Сотрудник сервиса может сделать вновь активным.')
    date_joined = models.DateTimeField('Дата создания аккаунта', default=timezone.now)

    # the name USERNAME_FIELD (e.g. not LOGIN_FIELD) are used, because AbstractBaseUser uses it.
    USERNAME_FIELD = 'login'
    # DEFAULT_GROUP_NAME used in childs classes for users with types
    DEFAULT_GROUP_NAME = None

    objects = UserManager()

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def _check_required_fields_is_not_empty(self) -> None:
        for field in self.REQUIRED_FIELDS:
            if not getattr(self, field):
                raise ValueError("The '%s' field is required." % field)

    def save(self, *args, **kwargs):
        self._check_required_fields_is_not_empty()

        self.phone = format_phone_to_rus_code(self.phone) if self.phone else None
        self.email = self.__class__.objects.normalize_email(self.email) if self.email else None

        return super().save(*args, **kwargs)

    @property
    def default_group(self):
        """ The group which user with type should belongs to. """
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
    def get_queryset(self):
        return super().get_queryset().filter(groups=self.model().default_group)

    def create_superuser(self, login, password, **extra_fields):
        raise NotImplementedError(f'{self.model().DEFAULT_GROUP_NAME} User cannot create superusers. ')

    def _create_user_obj(self, **fields):
        """
        Returns the user object which is ready to be saved.
        In **fields you have to specify all fields from USERNAME_FIELD and REQUIRED_FIELDS model attributes.
        Value from USERNAME_FIELD are going to save as login field.
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

    def create_user(self, password, **fields):
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
    class Meta:
        proxy = True

    objects = UserWithTypeManager()

    DEFAULT_GROUP_NAME = User.Types.EMPLOYEE.label
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']


class ClientUser(User):
    class Meta:
        proxy = True

    objects = UserWithTypeManager()

    DEFAULT_GROUP_NAME = User.Types.CLIENT.label
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['phone']
