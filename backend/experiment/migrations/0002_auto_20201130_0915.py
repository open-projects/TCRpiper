# Generated by Django 3.1.2 on 2020-11-30 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='reads_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='reads_2',
            field=models.IntegerField(default=0),
        ),
    ]
