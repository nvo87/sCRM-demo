# Generated by Django 3.2 on 2021-04-20 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user',
                 models.OneToOneField(help_text='Связанный аккаунт', on_delete=django.db.models.deletion.CASCADE,
                                      primary_key=True, related_name='profile', serialize=False, to='accounts.user')),
                ('first_name', models.CharField(max_length=64, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=64, verbose_name='Фамилия')),
                ('third_name', models.CharField(max_length=64, verbose_name='Отчество')),
            ],
        ),
    ]