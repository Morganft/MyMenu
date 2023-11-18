from django.contrib import admin
from .models import Receipt, IngredientType, Ingredient, Step, Tag

# Register your models here.
admin.site.register(Receipt)
admin.site.register(IngredientType)
admin.site.register(Ingredient)
admin.site.register(Step)
admin.site.register(Tag)
