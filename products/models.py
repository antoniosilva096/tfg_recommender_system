from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    asin = models.CharField(max_length=50, unique=True)
    title = models.TextField()
    categories = models.ManyToManyField(Category, related_name="products")
    price = models.FloatField()
    average_rating = models.FloatField(null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)  

    def __str__(self):
        return self.title
