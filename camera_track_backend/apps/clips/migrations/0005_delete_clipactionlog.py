# Generated by Django 4.1.7 on 2023-05-03 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clips', '0004_remove_clip_path'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClipActionLog',
        ),
    ]
