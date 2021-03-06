# Generated by Django 3.2 on 2021-04-29 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=[
            migrations.CreateModel(
                name='Membership',
                fields=[
                    ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                    ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ],
                options={
                    'db_table': 'accounts_user_groups',
                },
            ),
        ])
    ]
