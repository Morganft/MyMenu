from django.shortcuts import render, get_object_or_404

from .models import Receipt

# Create your views here.

def home(request):
  receipts = Receipt.objects.all()
  
  return render(request, 'home.html', {'receipts': receipts})

def receipt(request, pk):
  receipt = get_object_or_404(Receipt, pk=pk)
  return render(request, 'receipt.html', {'receipt': receipt})
