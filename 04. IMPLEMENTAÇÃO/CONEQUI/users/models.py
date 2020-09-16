from django.db import models
class Client(models.Model):
    usuario = models.CharField(max_length=255, null=False)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, null=True)
    cpf = models.CharField(max_length=255, null=False,unique=True)
    user_type = models.CharField(max_length=13, null=False,default='Comum')
    senha = models.CharField(max_length=50, null=False)
    fingerprint = models.CharField(max_length=1630,null=True,unique=True)
    inative = models.BooleanField(default=False)
    cod_telegram = models.TextField(max_length=10, null=True)
    
    def __str__(self):
        return self.usuario
