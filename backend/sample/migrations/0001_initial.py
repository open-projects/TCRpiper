# Generated by Django 2.2.12 on 2020-10-16 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_id', models.IntegerField()),
                ('sample_project', models.CharField(max_length=200)),
                ('sample_ident', models.CharField(max_length=200, unique=True)),
                ('sample_name', models.CharField(max_length=200)),
                ('sample_plate', models.CharField(max_length=200)),
                ('sample_well', models.CharField(max_length=200)),
                ('cell_number', models.IntegerField(default=0)),
                ('read_number', models.IntegerField(default=0)),
                ('smart_id', models.IntegerField(default=0)),
                ('alfa_subsample_ident', models.CharField(default='', max_length=200)),
                ('alfa_index_id', models.IntegerField(default=0)),
                ('beta_subsample_ident', models.CharField(default='', max_length=200)),
                ('beta_index_id', models.IntegerField(default=0)),
                ('comments', models.TextField(blank=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('owner', models.CharField(default='Unknown', max_length=200)),
            ],
        ),
    ]
