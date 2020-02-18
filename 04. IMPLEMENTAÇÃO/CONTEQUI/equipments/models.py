from django.db import models
from django.urls import reverse

# Create your models here.
class Equipment(models.Model):
    tag = models.CharField(max_length=10,help_text='title of message.')
    description = models.TextField()
    typ = models.CharField(max_length=10)
    maximum_time = models.IntegerField()

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('equipment_edit', kwargs={'pk': self.pk})