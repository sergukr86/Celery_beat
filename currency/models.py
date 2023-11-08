from django.db import models


# Create your models here.
class Rate(models.Model):
    vendor = models.CharField(max_length=20)
    cur_from = models.CharField(max_length=3)
    cur_to = models.CharField(max_length=3)
    sell = models.DecimalField(decimal_places=4, max_digits=9)
    buy = models.DecimalField(decimal_places=4, max_digits=9)
    date = models.DateField()
