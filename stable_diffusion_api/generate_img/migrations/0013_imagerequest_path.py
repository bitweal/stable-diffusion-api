# Generated by Django 4.2.7 on 2023-12-05 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate_img', '0012_remove_portqueue_queue_count_imagerequest_erorrs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagerequest',
            name='path',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
