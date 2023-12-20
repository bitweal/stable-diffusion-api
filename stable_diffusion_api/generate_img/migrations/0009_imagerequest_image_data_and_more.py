# Generated by Django 4.2.7 on 2023-12-04 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate_img', '0008_alter_imagerequest_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagerequest',
            name='image_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imagerequest',
            name='ip_address',
            field=models.GenericIPAddressField(),
        ),
    ]