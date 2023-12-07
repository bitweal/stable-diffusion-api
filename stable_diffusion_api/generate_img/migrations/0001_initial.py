# Generated by Django 4.2.7 on 2023-12-03 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusyPorts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.IntegerField(unique=True)),
                ('is_busy', models.BooleanField(default=False)),
            ],
        ),
    ]
