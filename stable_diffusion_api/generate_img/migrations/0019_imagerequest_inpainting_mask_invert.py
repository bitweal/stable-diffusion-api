# Generated by Django 4.2.7 on 2023-12-14 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate_img', '0018_alter_imagerequest_negative_prompt'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagerequest',
            name='inpainting_mask_invert',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
