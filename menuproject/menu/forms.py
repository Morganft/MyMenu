from django import forms
from .models import Ingredient, IngredientType

class NewIngredientForm(forms.ModelForm):
  amount = forms.DecimalField()
  types = IngredientType.objects.all()
  type_choices = [tuple[type.pk, type.name] for type in types]
  type = forms.ModelChoiceField(queryset=IngredientType.objects.all(), label="Ingredient")

  class Meta:
    model = Ingredient
    fields = ['type', 'amount']
