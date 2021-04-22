from django.db import migrations

from core.models import EmployeeRoles


def create_default_group(apps, schema_editor):
    GroupModel = apps.get_model('auth', 'group')

    for role in EmployeeRoles:
        group = GroupModel(name=role.label)
        group.save()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_groups'),
    ]

    operations = [
        migrations.RunPython(create_default_group)
    ]
