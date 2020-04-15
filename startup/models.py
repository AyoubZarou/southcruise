from django.db import models
import numpy as np

# Create your models here.

class Countries(models.Model):
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3)

    def __str__(self):
        return self.country_name


class PerformanceIndex(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, default=None)
    updated_weight = models.FloatField(default=0.0)
    higher_is_better = models.BooleanField(default=True)

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
    capital = models.FloatField(null=True)
    creation_date = models.DateTimeField(null=True)
    number_of_employees = models.IntegerField(null=True)
    maturity = models.CharField(max_length=100, default="Not specified")
    founder = models.CharField(max_length=200, blank=True, default="")
    customers = models.CharField(max_length=200, blank=True, default="")
    operationals = models.CharField(max_length=200, blank=True, default="")
    market_potential = models.CharField(max_length=200, blank=True, default="")
    investors = models.CharField(max_length=200, blank=True, default="")
    partnerships = models.CharField(max_length=200, blank=True, default="")
    innovation = models.BooleanField(default=False)
    impact = models.BooleanField(default=False)
    awards = models.CharField(max_length=400, blank=True, default="")
    growth_rate = models.FloatField(default=None, null=True, blank=True)
    reported_net_result = models.FloatField(default=None, null=True, blank=True)
    reported_net_debt = models.FloatField(default=None, null=True, blank=True)
    website = models.URLField(null=True, default="")
    presentation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class StartupActivityCountry(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    country = models.CharField(max_length=200, default="")

class StartupSector(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    sector = models.CharField(max_length=200, default="")


class StartupPerformance(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    index = models.CharField(max_length=200)
    year = models.IntegerField()
    value = models.FloatField()

    def __str__(self):
        return f'{self.startup}: {self.index}'
