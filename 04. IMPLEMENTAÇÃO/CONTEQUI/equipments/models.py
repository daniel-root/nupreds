from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Equipment_type(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
class Equipment(models.Model):
    tag = models.CharField(max_length=10)
    description = models.TextField()
    typ = models.ForeignKey('Equipment_type',on_delete=models.SET_NULL, null=True)
    maximum_time = models.IntegerField()

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('equipment_edit', kwargs={'pk': self.pk})

class Equipment_user(models.Model):
    loan = models.DateTimeField(blank=True)
    devolution = models.DateTimeField(blank=True,null=True)
    equiment = models.ForeignKey('Equipment',on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)