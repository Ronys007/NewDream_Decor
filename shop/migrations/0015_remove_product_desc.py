# Generated by Django 3.0.5 on 2022-10-08 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20221008_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='desc',
        ),
    ]
