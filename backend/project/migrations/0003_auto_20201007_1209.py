# Generated by Django 2.2.12 on 2020-10-07 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20201007_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.CharField(default='Unknown', max_length=200),
        ),
    ]
