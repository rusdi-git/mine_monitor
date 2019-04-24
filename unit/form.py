from django import forms
from datetime import date

from .models import Unit

class UnitForm(forms.ModelForm):
    date_assign = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y', attrs={'class':'date_input'}),
                                  input_formats=('%d/%m/%Y',),label='Date Assign')
    def clean_code(self):
        data = self.cleaned_data['code']
        if Unit.objects.filter(code=data).exists():
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