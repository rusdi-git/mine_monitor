from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView,DeleteView
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from .models import Unit
from .form import UnitForm,UnitFormSet
from .filter import UnitFilter
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

def unit_query(request):
    if request.method=='POST':
        pass
    else:
        unit_list=Unit.objects.all().order_by('id')
        unit_filter=UnitFilter(request.GET,queryset=unit_list)
        paginator=Paginator(unit_filter.qs,10)
        page=request.GET.get('page')
        try:
            data=paginator.page(page)
        except PageNotAnInteger:
            data=paginator.page(1)
        except EmptyPage:
            data=paginator.page(paginator.num_pages)
        page_query=Unit.objects.filter(id__in=[d.id for d in data])
        formset=UnitFormSet(queryset=page_query)
        context={'data':data,'formset':formset,'filterform':unit_filter.form}
        return render(request,'unit_query.html',context)

def set_mohh(request):
    if request.method=='POST':
        pass
    else:
        data=request.GET['data']