from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView,DeleteView
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Count

from .models import Unit
from .forms import UnitForm,UnitFormSet
from .filter import UnitFilter
from custom_code.views import generate_simple_summary
# Create your views here.
def home(request):
    return render(request,'home.html')

def unit_home(request):
    query = Unit.objects.values('type').annotate(jumlah=Count('id'))
    data=generate_simple_summary(query,'type')
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
        action=request.POST.get('action')
        if action=='activate':
            data_id=[]
            formset=UnitFormSet(request.POST,queryset=Unit.objects.all())
            if formset.is_valid():
                for form in formset.froms:
                    if form.cleaned_date.get('is_checked'):
                        data_id.append(form.cleaned_data.get('id').id)
                if data_id:
                    queryset=Unit.objects.filter(id__in=data_id)
                    pass
            return redirect('unithome')
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

def toggle_mohh(request,query=None):
    action=request.POST.get('action')
    if action=='execute_activation':
        data_id=[]