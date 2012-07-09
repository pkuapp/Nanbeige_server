from django.db import models

# Create your models here.
#Building Model
class Building(models.Model):
    name = models.CharField(max_length=30)
    university = models.ForeignKey(University)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
