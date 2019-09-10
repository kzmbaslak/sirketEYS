from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

class Calisan(models.Model):
    user = models.ForeignKey('auth.user', related_name='kullanici', on_delete=models.CASCADE, verbose_name = "Kullanıcı")
    tel = models.CharField(max_length = 10,verbose_name = "Telefon")
    yetki = models.ForeignKey('Yetki', related_name='yetki', on_delete=models.CASCADE,verbose_name = "Yetki")
    sgkNo = models.CharField(max_length=13, verbose_name = "Sgk No")
    maas = models.PositiveIntegerField()
    image = models.ImageField(null=True, blank=True)#imageField kullanmak için Pillow kütüphanesi yüklenmelidir. Sonrasında veritabanına veriler aktarılmalı. pip install Pillow 
    slug = models.SlugField(unique = True,editable = False, max_length= 160)

    def get_absolute_url(self):
        return reverse("calisan:detail",kwargs={'slug':self.slug})
    def get_create_url(self):
        return reverse("calisan:create")
    def get_update_url(self):
        return reverse("calisan:update",kwargs={'id':self.id})
    def get_delete_url(self):
        return reverse("calisan:delete",kwargs={'id':self.id})
    def get_passive_url(self):
        return reverse("calisan:passive",kwargs={'id':self.id})
    def get_active_url(self):
        return reverse("calisan:active",kwargs={'id':self.id})

    
    def get_unique_slug(self):
        slug = slugify(self.user.first_name.replace('ı','i'))
        unique_slug = slug
        counter = 1
        while Calisan.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(unique_slug,counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        super(Calisan, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.get_full_name()


class Yetki(models.Model):
    adi = models.CharField(max_length = 30,verbose_name = "Yetki Adı")

    def __str__(self):
        return self.adi


class Kart(models.Model):
    kodu = models.CharField(max_length = 64,verbose_name = "Kodu")
    calisan = models.ForeignKey('Calisan', related_name='KartCalisan', on_delete=models.CASCADE,verbose_name = "Çalışan")

    def get_delete_url(self):
        return reverse("calisan:kartDelete",kwargs={'id':self.id})
    def __str__(self):
        return self.kodu

class SgkPrim(models.Model):
    calisan = models.ForeignKey('Calisan',related_name='SgkPrimCalisan', on_delete=models.CASCADE,verbose_name = "Çalışan")
    odemeTarihi = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.calisan.user.first_name
class Izin(models.Model):
    calisan = models.ForeignKey('Calisan',related_name='IzinCalisan', on_delete=models.CASCADE,verbose_name = "Çalışan")
    kategori  = models.ForeignKey('Kategori', related_name='IzinKategori', on_delete=models.CASCADE,verbose_name = "Kategori")
    izinTarihi = models.DateTimeField()
    gun = models.PositiveIntegerField()

    

    def get_update_url(self):
        return reverse("calisan:izinUpdate",kwargs={'id':self.id})
    def __str__(self):
        return str(self.izinTarihi)
class Kategori(models.Model):
    adi = models.CharField(max_length = 50,verbose_name = "Kategori")

    def __str__(self):
        return self.adi
class MaasOdeme(models.Model):
    calisan = models.ForeignKey('Calisan',related_name='MaasOdemeCalisan', on_delete=models.CASCADE,verbose_name = "Çalışan")
    tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

#<Yetkilendirme fonksiyonları>
def getAuthorization(request,name):
    u = request.user
    yetki = 0
    if not u.is_authenticated:
        return -1
    elif u.is_superuser:
        return 15
    else:
        for i in u.groups.all():
            for j in i.permissions.all():
                #print(j.id,j.content_type_id,j.content_type,j.codename,j.name,j.id)
                #from django.contrib.auth.models import  Permission kullanılarak shell de content_type_id öğrenilebilir.
                if name in j.name[len(j.name)-len(name):]:
                    #print(j.id)
                    if "add" in j.name:
                        yetki += 1
                    if "change" in j.name:
                        yetki += 2
                    if "delete" in j.name:
                        yetki += 4
                    if "view" in j.name:
                        yetki += 8
        #print("----------------------------------------------")
        #print("id","content_type_id","content_type","codename","name")
        for i in u.user_permissions.all():
            
            #print(i.id,"-",i.content_type_id,"-",i.content_type,"-",i.codename,"-",i.name)

            if name in i.name[len(i.name)-len(name):]:
                print(i.id,"-",i.content_type_id,"-",i.content_type,"-",i.codename,"-",i.name)
                #print(j.id)
                if "add" in i.name:
                    yetki += 1
                if "change" in i.name:
                    yetki += 2
                if "delete" in i.name:
                    yetki += 4
                if "view" in i.name:
                    yetki += 8
        return yetki
def canView(authorization):
    return authorization >= 8
def canAdd(authorization):
    return authorization % 2 != 0
def canChange(authorization):
    return authorization == 2 or authorization == 3 or authorization == 6 or authorization == 7 or authorization == 10 or authorization == 11 or authorization == 14 or authorization == 15
def canDelete(authorization):
    return authorization == 4 or authorization == 5 or authorization == 6 or authorization == 7 or authorization == 12 or authorization == 13 or authorization == 14 or authorization == 15
#</yetkilendirme>