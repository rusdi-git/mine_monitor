from django import forms

from .models import Unit

class UnitForm(forms.ModelForm):
    date_assign = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y', attrs={'class':'date_input'}),
                                  input_formats=('%d/%m/%Y',))

    class Meta:
        model = Unit
        fields = '__all__'