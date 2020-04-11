from django.db import models


# Create your models here.

class Countries(models.Model):
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3)

    def __str__(self):
        return self.country_name


class PerformanceIndex(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, default="")
    updated_weight = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class CountryPerformance(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    year = models.IntegerField()
    value = models.FloatField()
    performance_index = models.ForeignKey(PerformanceIndex, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.country} : {self.performance_index}'


class Startup(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    capital = models.FloatField()
    creation_date = models.DateTimeField()
    number_of_employees = models.IntegerField()
    website = models.URLField()

    def __str__(self):
        return self.name


class StrartupPerformance(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    index = models.CharField(max_length=200)
    year = models.IntegerField()
    value = models.FloatField()

    def __str__(self):
        return f'{self.startup}: {self.index}'
