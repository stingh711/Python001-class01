from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)


class Comment(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    sentiments = models.FloatField()
    timestamp = models.DateField()
