# Generated by Django 3.0.5 on 2022-10-20 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20221020_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user_name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]