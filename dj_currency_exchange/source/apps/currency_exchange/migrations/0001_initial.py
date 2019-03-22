# Generated by Django 2.1.7 on 2019-03-14 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('code', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Provider',
                'db_table': 'provider',
                'verbose_name_plural': 'Providers',
            },
        ),
    ]
