# Generated by Django 3.2 on 2021-04-29 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_membership'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clubs.club'),
        ),
    ]
