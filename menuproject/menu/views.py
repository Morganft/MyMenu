from django.shortcuts import render, get_object_or_404, redirect

from .models import Receipt, IngredientType, Ingredient

# Create your views here.

def home(request):
  receipts = Receipt.objects.all()
  
  return render(request, 'home.html', {'receipts': receipts})

def receipt(request, pk):
  receipt = get_object_or_404(Receipt, pk=pk)
  return render(request, 'receipt.html', {'receipt': receipt})

def new_ingredient(request, receipt_pk):
  receipt = get_object_or_404(Receipt, pk=receipt_pk)

  if request.method == 'POST':
    amount = request.POST['amount']
    ingredient_type = IngredientType.objects.first()

    ingredient = Ingredient.objects.create(
      type=ingredient_type,
      amount=amount,
      receipt=receipt
    )

    return redirect('receipt', pk=receipt.pk)

  ingredient_types = IngredientType.objects.all()
  return render(request, 'new_ingredient.html', {'receipt': receipt, 'ingredient_types': ingredient_types})
