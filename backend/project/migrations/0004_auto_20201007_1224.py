# Generated by Django 2.2.12 on 2020-10-07 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20201007_1209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='project_name',
            new_name='name',
        ),
    ]