# Generated by Django 3.1.7 on 2021-03-25 15:33

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название клуба')),
                ('logo', models.ImageField(upload_to='', verbose_name='Логотип клуба')),
            ],
            options={
                'verbose_name': 'Клуб',
                'verbose_name_plural': 'Клубы',
            },
        ),
    ]
