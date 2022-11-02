from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True, null=False)

    def __str__(self):
        return f"{self.name}"


class Actions(models.Model):
    sum = models.DecimalField(decimal_places=2, max_digits=15)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    type = models.BooleanField()
