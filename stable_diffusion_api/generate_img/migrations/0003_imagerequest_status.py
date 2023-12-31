# Generated by Django 4.2.7 on 2023-12-04 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate_img', '0002_imagerequest_delete_busyports'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagerequest',
            name='status',
            field=models.CharField(choices=[('queued', 'Queued'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='queued', max_length=20),
        ),
    ]
