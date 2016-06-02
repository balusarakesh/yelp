from __future__ import unicode_literals

from django.db import models


class RatingModel(models.Model):
    username = models.TextField()
    userurl = models.TextField()
    rating = models.FloatField()
    review = models.TextField()
    restaurantname = models.TextField()
    restauranturl = models.TextField()

class DBStatusModel(models.Model):
    """
    Status of the DB.
    True - When data is being collected
    False - When the DB is free and no data is collected.
    """
    status = models.BooleanField()


class RestaurantModel(models.Model):
    name = models.TextField()
    expensivelevel = models.TextField()
    reviewcount = models.IntegerField()
    url = models.TextField()
    category = models.TextField()
    current_rating = models.FloatField()
    city = models.TextField()
    address = models.TextField()