# Generated by Django 2.2.3 on 2019-07-18 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlimFatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urunAdi', models.CharField(max_length=50, verbose_name='Ürün Adı')),
                ('urunAdedi', models.PositiveIntegerField()),
                ('birimFiyati', models.FloatField()),
                ('tarih', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(editable=False, max_length=60, unique=True)),
            ],
        ),
    ]