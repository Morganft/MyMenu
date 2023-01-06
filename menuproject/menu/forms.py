from django import forms
from .models import Ingredient, IngredientType, Receipt

class NewIngredientForm(forms.ModelForm):
  amount = forms.DecimalField()
  type = forms.ModelChoiceField(queryset=IngredientType.objects.all(), label="Ingredient")

  class Meta:
    model = Ingredient
    fields = ['type', 'amount']


class NewReceiptForm(forms.ModelForm):
  name = forms.CharField(max_length=80)
  description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'What is in your recipe?'}),
                                max_length=4000)
  class Meta:
    model = Receipt
    fields = ['name', 'description']
