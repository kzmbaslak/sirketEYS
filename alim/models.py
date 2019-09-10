from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.
class AlimFatura(models.Model):
    urunAdi = models.CharField(max_length=50, verbose_name = "Ürün Adı")
    urunAdedi = models.PositiveIntegerField()
    birimFiyati = models.FloatField()
    tarih = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique = True,editable = False, max_length= 60)

    def get_absolute_url(self):
        return reverse("alim:detail",kwargs={'slug':self.slug})
    def get_create_url(self):
        return reverse("alim:create")
    def get_update_url(self):
        return reverse("alim:update",kwargs={'id':self.id})
    def get_delete_url(self):
        return reverse("alim:delete",kwargs={'id':self.id})
    def get_unique_slug(self):
        slug = slugify(self.urunAdi.replace('ı','i'))
        unique_slug = slug
        counter = 1
        while AlimFatura.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(unique_slug,counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        super(AlimFatura, self).save(*args, **kwargs)
    
    def get_toplam_tutar(self):
        return self.birimFiyati*self.urunAdedi
    
    def __str__(self):
        return self.urunAdi
    
    class Meta:
        ordering = ['-tarih']