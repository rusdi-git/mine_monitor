from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Unit
from .form import UnitForm
# Create your views here.
def home(request):
    data = Unit.objects.all()
    return render(request,'home.html', {'data':data})

def unit_detil(request,pk):
    data = Unit.objects.get(pk=pk)
    return render(request,'unit_detil.html',{'data':data})

class UnitNew(CreateView):
    form_class = UnitForm
    template_name = 'unit_new.html'
    success_url = reverse_lazy('home')


class UnitUpdate(UpdateView):
    pass