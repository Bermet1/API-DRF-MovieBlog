# Generated by Django 3.2.9 on 2021-11-15 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieshots',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]