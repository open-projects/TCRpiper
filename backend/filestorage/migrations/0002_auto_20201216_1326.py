# Generated by Django 3.1.2 on 2020-12-16 13:26

from django.db import migrations, models
import filestorage.models


class Migration(migrations.Migration):

    dependencies = [
        ('filestorage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='experiment_id',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=filestorage.models.path2dir),
        ),
    ]
