# Generated by Django 2.2.3 on 2019-07-26 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alim', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alimfatura',
            options={'ordering': ['-tarih']},
        ),
    ]
