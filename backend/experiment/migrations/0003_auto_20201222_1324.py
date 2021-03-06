# Generated by Django 3.1.2 on 2020-12-22 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0002_auto_20201130_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='output_file',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='experiment',
            name='output_status',
            field=models.CharField(choices=[('incomplete', 'Incomplete'), ('ongoing', 'Ongoing'), ('ready', 'Ready')], default='incomplete', max_length=200),
        ),
    ]
