from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.views.generic import ListView

from .forms import NewIngredientForm, NewReceiptForm, NewStepForm, NewIngredientTypeForm
from .models import Receipt, IngredientType, Step


# Create your views here.
def home(request):
    receipts = Receipt.objects.all()

    return render(request, 'home.html', {'receipts': receipts})


class ReceiptsListView(ListView):
    model = Receipt
    context_object_name = 'receipts'
    template_name = 'receipts.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = Receipt.objects.all().order_by('name')
        return queryset


def receipt(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    return render(request, 'receipt.html', {'receipt': receipt})


class IngredientTypesListView(ListView):
    model = IngredientType
    context_object_name = 'ingredient_types'
    template_name = 'ingredient_types.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = IngredientType.objects.all().order_by('name')
        return queryset


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
def new_ingredient_type(request):
    if request.method == 'POST':
        form = NewIngredientTypeForm(request.POST)
        if form.is_valid():
            ingredient_type = form.save(commit=False)
            ingredient_type.save()

            return redirect('ingredient_types')
    else:
        form = NewIngredientTypeForm()

    return render(request, 'new_ingredient_type.html', {'form': form})


@login_required
def new_receipt(request):
    if request.method == 'POST':
        form = NewReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.created_by = request.user
            receipt.save()

            return redirect('receipt', pk=receipt.pk)
    else:
        form = NewReceiptForm()

    return render(request, 'new_receipt.html', {'form': form})


@login_required
def new_step(request, receipt_pk):
    receipt = get_object_or_404(Receipt, pk=receipt_pk)
    if request.method == 'POST':
        form = NewStepForm(request.POST)
        if form.is_valid():
            step = form.save(commit=False)
            step.receipt = receipt
            step.save()
            return redirect('receipt', pk=receipt_pk)
    else:
        form = NewStepForm()
    return render(request, 'new_step.html', {'receipt': receipt, 'form': form})


@method_decorator(login_required, name='dispatch')
class StepUpdateView(UpdateView):
    model = Step
    fields = ('name', 'description')
    template_name = 'edit_step.html'
    pk_url_kwarg = 'step_pk'
    context_object_name = 'step'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(receipt__created_by=self.request.user)

    def form_valid(self, form):
        step = form.save(commit=False)
        step.save()
        return redirect('receipt', pk=step.receipt.pk)


@method_decorator(login_required, name='dispatch')
class IngredientTypeUpdateView(UpdateView):
    model = IngredientType
    fields = ('name',)
    template_name = 'edit_ingredient_type.html'
    pk_url_kwarg = 'ingredient_type_pk'
    context_object_name = 'ingredient_type'

    def form_valid(self, form):
        ingredient_type = form.save(commit=False)
        ingredient_type.save()
        return redirect('ingredient_types')
