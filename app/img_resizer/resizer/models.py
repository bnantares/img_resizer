from django.db import models
from django.utils.text import slugify
from time import time

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Picture(models.Model):
    picture_url = models.URLField('URL', max_length=500, blank=True)
    img = models.ImageField('Фотография', upload_to='images/', blank=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    wo_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.wo_id)
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.img.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'



