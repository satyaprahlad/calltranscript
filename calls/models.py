from django.db import models


class Country(models.Model):
    name =  models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class State(models.Model):
    name =  models.CharField(max_length=100)
    country =  models.ForeignKey(Country, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} @ {self.created_at}"


class CallDetails(models.Model):
    customer_id = models.CharField(max_length=50)
    call_date = models.DateTimeField(null=True)
    call_type = models.CharField(max_length=100)
    transcript = models.TextField(max_length=10000)
    subject_line = models.TextField(max_length=1000)
    aht =  models.TextField(max_length=100)
    summary =  models.TextField(max_length=10000)
    def __str__(self):
        return f"{self.customer_id} @ {self.call_date}@ {self.call_type}"