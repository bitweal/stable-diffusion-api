# Generated by Django 4.2.7 on 2023-12-04 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate_img', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_generate', models.TextField(max_length=10)),
                ('prompt', models.TextField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='BusyPorts',
        ),
    ]
