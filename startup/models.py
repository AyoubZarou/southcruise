from django.db import models

# Create your models here.

class Countries(models.Model):
    country = models.ForeignKey()
    year = models.IntegerField()
    GDP_growth = models.FloatField()

    def __str__(self):
        return self.country_name

class CountryPerformance(models.Model):
    country_name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2)
    country_code_2 = models.CharField(max_length=3)
    country = models.ForeignKey(Countries)
    year = models.IntegerField()
    GDP_growth = models.FloatField()

class Startup(models.Model):
    pass




