from django.shortcuts import render

from .models import Receipt

# Create your views here.

def home(request):
  receipts = Receipt.objects.all()
  
  return render(request, 'home.html', {'receipts': receipts})

