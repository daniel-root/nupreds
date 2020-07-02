from django.db import models
from django.urls import reverse
from users.models import Client

class Equipment_type(models.Model):
    name = models.CharField(max_length=20,unique=True)
    inative = models.BooleanField(default=False)
    time_maximum = models.IntegerField(default=0)

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
    maximum_time = models.IntegerField(default=5)
    inative = models.BooleanField(default=False)
    status =  models.CharField(max_length=9, null=False, choices=STATUS_CHOICES,default='Livre')
    amount_of_loans = models.IntegerField(default=0)
    
    '''
    def contact_default():
    return {"email": "to1@example.com"}
    contact_info = JSONField("ContactInfo", default=contact_default)
    '''

    def __int__(self):
        return self.id

class Equipment_user(models.Model):
    loan = models.DateTimeField(blank=True)
    devolution = models.DateTimeField(blank=True,null=True)
    equipment = models.ForeignKey('Equipment',on_delete=models.SET_NULL, null=True)
    user_loan = models.ForeignKey(Client,on_delete=models.SET_NULL, null=True,related_name='emprestimo')
    user_devolution = models.ForeignKey(Client,on_delete=models.SET_NULL, null=True,related_name='devolução')
    amount_of_loans = models.IntegerField(default=0)
    limit_time = models.DateTimeField(blank=True,null=True)

