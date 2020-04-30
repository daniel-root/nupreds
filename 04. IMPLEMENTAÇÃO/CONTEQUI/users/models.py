from django.conf import settings
from django.db import models
class Client(models.Model):
    TYPES_CHOICES = (
        (u'Comum', u'Comum'),
        (u'Administrador', u'Administrador'),
        (u'Super', u'Super'),
    )
    usuario = models.CharField(max_length=255, null=False,unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, null=True)
    whatsapp = models.CharField(max_length=20, null=True)
    cpf = models.CharField(max_length=255, null=False,unique=True)
    #data_de_nascimento = models.DateField(null=False)
    user_type = models.CharField(max_length=13, null=False, choices=TYPES_CHOICES,default='Comum')
    senha = models.CharField(max_length=50, null=False)
    #repetir_senha = models.CharField(max_length=50, null=False, default="")
    inative = models.BooleanField(default=False)
    
    def __str__(self):
        return self.usuario
