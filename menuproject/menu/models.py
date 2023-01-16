from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from markdown import markdown


# Create your models here.
class Receipt(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        User, related_name='receipts', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

# class Board(models.Model):
#   name = models.CharField(max_length=30, unique=True)
#   description = models.CharField(max_length=100)
#   receipts = models.ManyToMany(Receipt)


class IngredientType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    type = models.ForeignKey(IngredientType, on_delete=models.DO_NOTHING)
    amount = models.CharField(max_length=30)
    receipt = models.ForeignKey(
        Receipt, related_name='ingridients', on_delete=models.DO_NOTHING)


class Step(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=4000)
    receipt = models.ForeignKey(
        Receipt, related_name='steps', on_delete=models.DO_NOTHING)

    def get_description_as_markdown(self):
        return mark_safe(markdown(self.description, safe_mode='escape'))
