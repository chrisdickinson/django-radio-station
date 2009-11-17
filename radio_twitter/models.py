from django.db import models
import twitter

class Credential(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField()
    def __unicode__(self):
        return u'%s' % self.username

    def get_api(self):
        api = twitter.Api(username=self.username, password=self.password)
        return api

class PendingUpdate(models.Model):
    status = models.CharField(max_length=140)
    has_posted = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now=True)
 
