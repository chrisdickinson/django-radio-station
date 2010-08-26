from django.db import models
from radio.station.models import Schedule
from django.contrib.auth.models import User

class Role(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    weight = models.PositiveIntegerField()
    class Meta:
        ordering = ['weight']

    def __unicode__(self):
        return u'%s' % self.title

class StaffRoleRelation(models.Model):
    user = models.ForeignKey(User)
    role = models.ForeignKey(Role)
    schedule = models.ManyToManyField(Schedule, blank=True)

    def get_email(self):
        return self.role.email if self.role.email is not None else self.user.email

    def get_phone(self):
        return self.role.phone
