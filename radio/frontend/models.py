from django.db import models

class Ad(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='usr/ads', help_text='300px by 300px')
    link = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()

