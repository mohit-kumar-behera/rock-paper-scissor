# Generated by Django 3.0.7 on 2020-12-16 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0004_auto_20201216_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='u_id',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]