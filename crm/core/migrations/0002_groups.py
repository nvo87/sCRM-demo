from django.db import migrations

from core.models import User


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    def create_default_group(apps, schema_editor):
        GroupModel = apps.get_model('auth', 'group')

        for _type in User.Types:
            group = GroupModel(name=_type.label)
            group.save()

    operations = [
        migrations.RunPython(create_default_group)
    ]
