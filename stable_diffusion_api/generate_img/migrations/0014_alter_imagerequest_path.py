# Generated by Django 4.2.7 on 2023-12-05 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate_img', '0013_imagerequest_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerequest',
            name='path',
            field=models.TextField(),
        ),
    ]
