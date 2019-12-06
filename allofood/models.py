
from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    telephone = models.IntegerField()
    address = models.CharField(max_length=250)
    image = models.CharField(max_length=250, default='avatar.png')
    password = models.CharField(max_length=250)
    confirmed = models.BooleanField(default=False)
    token = models.CharField(max_length=250)
    cart = models.TextField(null=True)


class Restaurant(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    rating = models.IntegerField()
    type = models.CharField(max_length=100)
    image = models.CharField(max_length=250)
    type_icon = models.CharField(max_length=250)
    link = models.CharField(max_length=250)
    summary = models.CharField(max_length=250, blank=True)
    sliders = models.CharField(max_length=250, blank=True)


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    ingredients = models.CharField(max_length=250)
    image = models.CharField(max_length=250)
    type = models.CharField(max_length=100)
    type_order = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField()
    subtotal = models.IntegerField()
    address = models.CharField(max_length=250)
    telephone = models.IntegerField()
    payed = models.BooleanField(default=False)


class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()

