from django.db import models


class Companies(models.Model):
    company_name = models.CharField(max_length=200)
    company_description = models.CharField(max_length=2000)
    company_logo = models.CharField(max_length=500)

    def __str__(self):
        return self.company_name


class Employees(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    photo = models.CharField(max_length=500)
    position = models.CharField(max_length=200)
    salary = models.FloatField()
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + '' + self.last_name
