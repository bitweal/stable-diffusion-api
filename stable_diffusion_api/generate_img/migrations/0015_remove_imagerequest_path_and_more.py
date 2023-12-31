# Generated by Django 4.2.7 on 2023-12-07 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate_img', '0014_alter_imagerequest_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagerequest',
            name='path',
        ),
        migrations.AddField(
            model_name='imagerequest',
            name='denoising_strength',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=3),
        ),
        migrations.AddField(
            model_name='imagerequest',
            name='path_to_img',
            field=models.TextField(default=''),
        ),
    ]
