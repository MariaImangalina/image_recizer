from django.db import models
from django.urls import reverse


class Image(models.Model):
    name = models.CharField(max_length=255, blank=True)
    img = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('images:resize', kwargs={'pk':self.pk})
