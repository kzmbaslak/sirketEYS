# Generated by Django 2.2.3 on 2019-08-08 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proje', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='talep',
            name='maliyet',
            field=models.PositiveIntegerField(default=0, verbose_name='Maliyet'),
            preserve_default=False,
        ),
    ]