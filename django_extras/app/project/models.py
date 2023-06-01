from django.db import models
from django.utils.text import slugify


class BooksModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    user = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if 'request' in kwargs:
            request = kwargs.pop('request')
            self.user = request.user
        self.slug = slugify(self.name)
        super(BooksModel, self).save(*args, **kwargs)
