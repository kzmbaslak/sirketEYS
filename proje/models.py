from django.db import models
from calisan.models import Calisan, Yetki
from django.utils.text import slugify
from django.urls import reverse
from ciro.models import *

# Create your models here.

class Proje(models.Model):
    adi = models.CharField(max_length=120)
    yoneticiCalisan = models.ForeignKey('calisan.Calisan', related_name='yonetici', on_delete=models.CASCADE,verbose_name="Yönetici")
    slug = models.SlugField(unique = True,editable = False, max_length= 130)

    def get_absolute_url(self):
        return reverse("proje:detail",kwargs={'slug':self.slug})
    def get_create_url(self):
        return reverse("proje:create")
    def get_update_url(self):
        return reverse("proje:update",kwargs={'id':self.id})
    def get_delete_url(self):
        return reverse("proje:delete",kwargs={'id':self.id})

    def get_unique_slug(self):
        slug = slugify(self.adi.replace('ı','i'))
        unique_slug = slug
        counter = 1
        while Proje.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(unique_slug,counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        super(Proje, self).save(*args, **kwargs)

    def __str__(self):
        return self.adi

class Ekip(models.Model):
    adi = models.CharField(max_length = 50)
    proje = models.ForeignKey('Proje',related_name='EkipProje',on_delete=models.CASCADE,verbose_name="Proje")

    def __str__(self):
        return self.adi

class EkipUye(models.Model):
    ekip = models.ForeignKey('Ekip',related_name='ekip',on_delete=models.CASCADE, verbose_name="Ekip")
    calisan = models.ForeignKey('calisan.Calisan',related_name='EkipUyeCalisan',on_delete=models.CASCADE, verbose_name="Çalışan")
    yetki = models.ForeignKey('calisan.Yetki',related_name='EkipUyeYetki',on_delete=models.CASCADE,verbose_name="Yetki")

    def __str__(self):
        return self.calisan.user.first_name
    
class Talep(models.Model):
    calisan =  models.ForeignKey('calisan.Calisan',related_name='TalepCalisan',on_delete=models.CASCADE, verbose_name="Çalışan")
    baslik = models.CharField(max_length=150,verbose_name="Başlık")
    proje = models.ForeignKey('Proje',related_name='TalepProje',on_delete=models.CASCADE,verbose_name="Proje")
    text = models.TextField(verbose_name="Açıklama")
    tarihi = models.DateTimeField(auto_now_add=True)
    kabulDurumu = models.NullBooleanField(verbose_name="Kabul Durumu")
    maliyet = models.PositiveIntegerField(verbose_name="Maliyet")
    
    def get_absolute_url(self):
        return reverse("proje:talepDetail",kwargs={'id':self.id})

    def save(self, *args, **kwargs):
        ProjeGider.objects.create(talep = self).save()
        super(Talep, self).save(*args, **kwargs)

    def __str__(self):
        return self.baslik

