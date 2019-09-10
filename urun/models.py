from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Urun(models.Model):
    adi = models.CharField(max_length = 120,verbose_name= "Ürün Adı")
    birimFiyati = models.FloatField()
    stokMiktari = models.IntegerField()
    slug = models.SlugField(unique = True,editable = False, max_length= 130)

    def get_update_url(self):
        return reverse("urun:update",kwargs={"slug":self.slug})
    def get_delete_url(self):
        return reverse("urun:delete",kwargs={"id":self.id})
    def get_unique_slug(self):
        slug = slugify(self.adi.replace('ı','i'))
        unique_slug = slug
        counter = 1
        while Urun.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(unique_slug,counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        super(Urun, self).save(*args, **kwargs)

    def __str__(self):
        return self.adi
