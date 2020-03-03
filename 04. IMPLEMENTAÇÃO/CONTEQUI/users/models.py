from django.db import models
from django.contrib.auth.models import User
class User(models.Model):
    SEXO_CHOICES = (
        (u'Masculino', u'Masculino'),
        (u'Feminino', u'Feminino'),
    )
    #user = models.OneToOneField(User, related_name='profile')
    nome = models.CharField(max_length=255, null=False)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, null=True)
    cpf = models.CharField(max_length=255, null=False)
    data_de_nascimento = models.DateField(null=False)
    sexo = models.CharField(max_length=9, null=False, choices=SEXO_CHOICES)
    senha = models.CharField(max_length=50, null=False)
    usuario = models.CharField(max_length=255, null=False)

    def __unicode__(self):
        return self.nome
