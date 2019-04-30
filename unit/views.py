from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView,DeleteView

from .models import Unit
from .form import UnitForm
# Create your views here.
def home(request):
    return render(request,'home.html')

def unit_home(request):
    data = Unit.objects.all()
    return render(request,'unit_home.html',{'data':data})

def unit_detil(request,pk):
    data = Unit.objects.get(pk=pk)
    return render(request,'unit_detil.html',{'data':data})

class UnitNew(CreateView):
    form_class = UnitForm
    template_name = 'unit_new.html'
    success_url = reverse_lazy('unithome')


class UnitUpdate(UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'unit_update.html'
    context_object_name = 'unit'
    def get_success_url(self):
        member=self.object
        return reverse_lazy('unitdetil',kwargs={'pk':member.pk})

class UnitDelete(DeleteView):
    model = Unit
    success_url = reverse_lazy('unithome')
    context_object_name = 'unit'
    template_name = 'unit_delete.html'