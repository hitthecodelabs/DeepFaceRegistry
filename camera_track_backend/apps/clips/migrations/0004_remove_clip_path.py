# Generated by Django 4.1.7 on 2023-05-03 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clips', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clip',
            name='path',
        ),
    ]
