from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import NewIngredientForm, NewReceiptForm
from .models import Receipt, IngredientType


# Create your views here.
def home(request):
    receipts = Receipt.objects.all()

    return render(request, 'home.html', {'receipts': receipts})


def receipts(request):
    receipts = Receipt.objects.all()

    return render(request, 'receipts.html', {'receipts': receipts})


def receipt(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    return render(request, 'receipt.html', {'receipt': receipt})


@login_required
def new_ingredient(request, receipt_pk):
    receipt = get_object_or_404(Receipt, pk=receipt_pk)

    if request.method == 'POST':
        form = NewIngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.receipt = receipt
            ingredient.save()

            return redirect('receipt', pk=receipt.pk)
    else:
        form = NewIngredientForm()

    ingredient_types = IngredientType.objects.all()
    return render(request, 'new_ingredient.html', {'receipt': receipt,
                                                   'ingredient_types': ingredient_types,
                                                   'form': form})


@login_required
def new_receipt(request):
    if request.method == 'POST':
        form = NewReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.created_by = User.objects.first()
            receipt.save()

            return redirect('home')
    else:
        form = NewReceiptForm()

    return render(request, 'new_receipt.html', {'form': form})
