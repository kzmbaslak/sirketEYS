# Generated by Django 2.2.3 on 2019-07-18 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Calisan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel', models.CharField(max_length=10, verbose_name='Telefon')),
                ('sgkNo', models.CharField(max_length=13, verbose_name='Sgk No')),
                ('maas', models.PositiveIntegerField()),
                ('resim', models.ImageField(blank=True, null=True, upload_to='')),
                ('slug', models.SlugField(editable=False, max_length=160, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kullanici', to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
        ),
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adi', models.CharField(max_length=50, verbose_name='Kategori')),
            ],
        ),
        migrations.CreateModel(
            name='Yetki',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adi', models.CharField(max_length=30, verbose_name='Yetki Adı')),
            ],
        ),
        migrations.CreateModel(
            name='SgkPrim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('odemeTarihi', models.DateTimeField(auto_now_add=True)),
                ('calisan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SgkPrimCalisan', to='calisan.Calisan', verbose_name='Çalışan')),
            ],
        ),
        migrations.CreateModel(
            name='MaasOdeme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarihi', models.DateTimeField(auto_now_add=True)),
                ('calisan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MaasOdemeCalisan', to='calisan.Calisan', verbose_name='Çalışan')),
            ],
        ),
        migrations.CreateModel(
            name='Kart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kodu', models.CharField(max_length=64, verbose_name='Kodu')),
                ('calisan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='KartCalisan', to='calisan.Calisan', verbose_name='Çalışan')),
            ],
        ),
        migrations.CreateModel(
            name='Izin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('izinTarihi', models.DateTimeField(auto_now_add=True)),
                ('gun', models.PositiveIntegerField()),
                ('calisan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='IzinCalisan', to='calisan.Calisan', verbose_name='Çalışan')),
                ('kategori', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='IzinKategori', to='calisan.Kategori', verbose_name='Kategori')),
            ],
        ),
        migrations.AddField(
            model_name='calisan',
            name='yetki',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yetki', to='calisan.Yetki', verbose_name='Yetki'),
        ),
    ]
