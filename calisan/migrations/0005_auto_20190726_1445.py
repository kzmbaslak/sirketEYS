# Generated by Django 2.2.3 on 2019-07-26 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calisan', '0004_auto_20190726_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='izin',
            name='izinTarihi',
            field=models.DateTimeField(),
        ),
    ]
