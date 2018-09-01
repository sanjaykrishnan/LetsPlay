from django.contrib.auth.models import User
from django.db import models


class SportsCentre(models.Model):
    """SportsCentre having image"""
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=250)
    address = models.TextField(max_length=250)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    """Booking object related to SportsCentre."""
    name = models.CharField(max_length=200)
    sports_centre = models.ForeignKey(SportsCentre, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    date = models.DateField()
    slot = models.CharField(max_length=100)

    def __str__(self):
        return self.name