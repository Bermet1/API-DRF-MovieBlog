# Generated by Django 3.2.9 on 2021-11-19 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_alter_movieshots_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]