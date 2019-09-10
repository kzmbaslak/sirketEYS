from django.db import models
from proje.models import *
from django.utils.text import slugify
# Create your models here.

class ProjeGider(models.Model):
    talep = models.ForeignKey('proje.Talep', related_name='ProjeGiderTalep', on_delete=models.CASCADE,verbose_name="Talep")
    tarih = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique = True,editable = False, max_length= 50)

    def get_unique_slug(self):
        slug = slugify(self.talep.baslik.replace('ı','i'))
        unique_slug = slug
        counter = 1
        while ProjeGider.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(unique_slug,counter)
            counter += 1
        return unique_slug
    
    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        super(ProjeGider, self).save(*args, **kwargs)