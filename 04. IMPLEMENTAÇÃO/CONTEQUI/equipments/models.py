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


class Client(models.Model):
    SEXO_CHOICES = (
        (u'Masculino', u'Masculino'),
        (u'Feminino', u'Feminino'),
    )
    usuario = models.CharField(max_length=255, null=False)
    nome = models.CharField(max_length=255, null=False)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, null=True)
    cpf = models.CharField(max_length=255, null=False)
    data_de_nascimento = models.DateField(null=False)
    sexo = models.CharField(max_length=9, null=False, choices=SEXO_CHOICES)
    senha = models.CharField(max_length=50, null=False)
    

    def __str__(self):
       return self.usuario

    def get_absolute_url(self):
        return reverse('equipment_edit', kwargs={'pk': self.pk})

class Equipment_user(models.Model):
    loan = models.DateTimeField(blank=True)
    devolution = models.DateTimeField(blank=True,null=True)
    equiment = models.ForeignKey('Equipment',on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('Client',on_delete=models.SET_NULL, null=True)