from django.db import models


class StarRatings(models.Model):
    username = models.CharField(max_length=100)
    comments = models.CharField(max_length=250)
    rating = models.CharField(max_length=2)