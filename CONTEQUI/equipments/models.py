from django.db import models
from django.urls import reverse
from users.models import Client

# Create your models here.
class Equipment_type(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
class Equipment(models.Model):
    STATUS_CHOICES = (
        (u'Livre', u'Livre'),
        (u'Ocupado', u'Ocupado'),
        (u'Atrasado', u'Atrasado'),
    )
    tag = models.CharField(max_length=10)
    description = models.TextField()
    type_equipment = models.ForeignKey('Equipment_type',on_delete=models.SET_NULL, null=True)
    maximum_time = models.IntegerField()
    inative = models.BooleanField(default=False)
    status =  models.CharField(max_length=9, null=False, choices=STATUS_CHOICES,default='Livre')
    amount_of_loans = models.IntegerField(default=0)

    def __int__(self):
        return self.id

class Equipment_user(models.Model):
    loan = models.DateTimeField(blank=True)
    devolution = models.DateTimeField(blank=True,null=True)
    equiment = models.ForeignKey('Equipment',on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(Client,on_delete=models.SET_NULL, null=True,related_name='emprestimo')
    usuario2 = models.ForeignKey(Client,on_delete=models.SET_NULL, null=True,related_name='devolução')
    amount_of_loans = models.IntegerField(default=0)
