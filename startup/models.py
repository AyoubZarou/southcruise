from django.db import models


# Create your models here.

class Countries(models.Model):
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3)

    def __str__(self):
        return self.country_name


class CountryPerformance(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    year = models.IntegerField()
    value = models.FloatField()
    performance_index = models.CharField(max_length=200)


class Startup(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    capital = models.FloatField()
    creation_date = models.DateTimeField()
    number_of_employees = models.IntegerField()
    website = models.URLField()



