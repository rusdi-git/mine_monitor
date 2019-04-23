from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .form import UnitForm

# Create your views here.
def home(request):
    return render(request,'home.html')

class UnitNew(CreateView):
    form_class = UnitForm
    template_name = 'unit_new.html'
    success_url = reverse_lazy('home')