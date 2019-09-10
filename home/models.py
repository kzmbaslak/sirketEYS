from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse
# Create your models here.

class Duyuru(models.Model):
    baslik = models.CharField(max_length = 120,verbose_name="Başlık")
    text = RichTextField(verbose_name="İçerik")
    tarih = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique = True,editable=False)
    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        return reverse("home:detail",kwargs={"slug":self.slug})

    def get_create_url(self):
        return reverse("home:create")
    def get_update_url(self):
        return reverse("home:update",kwargs={"slug":self.slug})
    def get_delete_url(self):
        return reverse("home:delete",kwargs={"slug":self.slug})
    def get_unique_slug(self):
        slug = slugify(self.baslik.replace('ı','i'))
        uniq_slug = slug
        counter = 1
        while Duyuru.objects.filter(slug = uniq_slug).exists():
            print("GIRDI")
            uniq_slug = '{}-{}'.format(slug,counter)
            counter += 1
        return uniq_slug
    
    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        super(Duyuru, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['-tarih']