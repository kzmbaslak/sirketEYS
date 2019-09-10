from django.db import models
from urun.models import Urun
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class SatimFatura(models.Model):
    urun = models.ForeignKey('urun.Urun', related_name='SatimFaturaUrun', on_delete=models.CASCADE,verbose_name = "Ürün")
    adedi = models.PositiveIntegerField()
    aliciAdi = models.CharField(max_length = 50)
    tarihi = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique = True,editable = False, max_length= 130)

    def get_absolute_url(self):
        return reverse("satim:detail",kwargs={'slug':self.slug})
    def get_create_url(self):
        return reverse("satim:create")
    def get_update_url(self):
        return reverse("satim:update",kwargs={'id':self.id})
    def get_delete_url(self):
        return reverse("satim:delete",kwargs={'id':self.id})

    def get_unique_slug(self):
        slug = slugify(self.urun.adi.replace('ı','i'))
        unique_slug = slug
        counter = 1
        while SatimFatura.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(unique_slug,counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        super(SatimFatura, self).save(*args, **kwargs)
    def get_toplam_tutar(self):
        return self.adedi*self.urun.birimFiyati
    def __str__(self):
        return self.urun.adi
    
    class Meta:
        ordering = ['-tarihi']