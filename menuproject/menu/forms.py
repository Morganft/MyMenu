from django import forms

from .models import Ingredient, IngredientType, Receipt, Step
from .widgets import ImageWidget


class NewIngredientForm(forms.ModelForm):
    amount = forms.DecimalField()
    type = forms.ModelChoiceField(
        queryset=IngredientType.objects.all(), label="Ingredient")

    class Meta:
        model = Ingredient
        fields = ['type', 'amount']


class NewIngredientTypeForm(forms.ModelForm):
    forms.CharField(max_length=80)

    class Meta:
        model = IngredientType
        fields = ['name',]


class NewReceiptForm(forms.ModelForm):
    name = forms.CharField(max_length=80)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'What is in your recipe?'}),
                                  max_length=4000)

    class Meta:
        model = Receipt
        fields = ['name', 'amount', 'description']


class NewStepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['name', 'description', 'image']
        widgets = {
            'image': ImageWidget()
        }
