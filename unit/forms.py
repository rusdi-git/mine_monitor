from django import forms
from django.forms.models import modelformset_factory
from datetime import date

from .models import Unit

class UnitForm(forms.ModelForm):
    date_assign = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y', attrs={'class':'date_input'}),
                                  input_formats=('%d/%m/%Y',),label='Date Assign')
    def clean_code(self):
        data = self.cleaned_data['code']
        existsing_name = Unit.objects.filter(code=data).exists()
        is_update = self.instance.pk
        if not is_update and existsing_name or is_update and existsing_name and self.instance.code!=data:
            self.add_error('code','Unit with this code already exist, please choose another code')
        else:
            return data

    def clean_date_assign(self):
        data = self.cleaned_data['date_assign']
        today = date.today()
        if data>today:
            self.add_error('date_assign','This date is not yet happen, max date is {}'.
                           format(today.strftime('%d/%m/%Y')))
        else:
            return data


    class Meta:
        model = Unit
        fields = '__all__'


UnitFormSetBase = modelformset_factory(Unit,extra=0,exclude=('code','type','date_assign'))

class UnitFormSet(UnitFormSetBase):
    def add_fields(self,form,index):
        super().add_fields(form,index)
        form.fields['is_checked']=forms.BooleanField(required=False,
                                                     widget=forms.CheckboxInput(attrs={'class':'CheckChoice'}))

class SetMOHHFormSet(UnitFormSetBase):
    def add_fields(self,form,index):
        super().add_fields(form,index)
        form.fields['start_mohh']=forms.DateField(widget=forms.DateInput(attrs={'class':'date_input'},
                                                                         format='%d/%m/%Y'),
                                                  input_formats=('%d/%m/%Y'))

