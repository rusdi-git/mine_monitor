from django import forms
from django.forms.models import modelformset_factory
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone

from .models import Unit,Mohh

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

class StartMOHHFormSet(UnitFormSetBase):
    def add_fields(self,form,index):
        super().add_fields(form,index)
        form.fields['start_mohh'] = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(date_format='%d/%m/%Y',
                                                                              date_attrs={
                                                                                  'class': 'date_input'},
                                                                              time_format='%H:%M',
                                                                              time_attrs={
                                                                                  'class': 'time_input'}),
                                             input_date_formats=('%d/%m/%Y',),
                                             input_time_formats=('%H:%M',),
                                             initial=timezone.now(),
                                                             )

    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            start_event=form.cleaned_data.get('start_mohh')
            last_mohh=form.instance.get_latest_mohh()
            if last_mohh and not last_mohh.end:
                form.add_error('start_mohh','This unit is still active')
            if start_event>timezone.now():
                form.add_error('start_mohh','This date is not yet happened')
            if last_mohh and start_event<last_mohh.end:
                form.add_error('start_mohh','Start Date is Earlier than latest end date MOHH')

    def save(self):
        for form in self.forms:
            unit=form.instance
            start=form.cleaned_data.get('start_mohh')
            Mohh.objects.create(unit=unit,start=start)



class EndMOHHFormSet(UnitFormSetBase):
    def add_fields(self,form,index):
        super().add_fields(form,index)
        form.fields['end_mohh'] = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(date_format='%d/%m/%Y',
                                                                              date_attrs={
                                                                                  'class': 'date_input'},
                                                                              time_format='%H:%M',
                                                                              time_attrs={
                                                                                  'class': 'time_input'}),
                                             input_date_formats=('%d/%m/%Y',),
                                             input_time_formats=('%H:%M',),
                                             initial=timezone.now(),
                                                             )

    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            end_event=form.cleaned_data.get('end_mohh')
            last_mohh=form.instance.get_latest_mohh()
            if last_mohh and last_mohh.end or not last_mohh:
                form.add_error('end_mohh','This unit is still non-active')
            if end_event>timezone.now():
                form.add_error('end_mohh','This time is not yet happened')
            if last_mohh and end_event<last_mohh.end:
                form.add_error('end_mohh','End Date is Earlier than latest end date MOHH')

    def save(self):
        for form in self.forms:
            unit=form.instance
            mohh=unit.get_latest_mohh()
            end=form.cleaned_data.get('start_mohh')
            mohh.end=end
            mohh.save()

class MOHHForm(forms.ModelForm):
    def clean_start(self):
        data=self.cleaned_data.get('start')
        previous = Mohh.objects.filter(id__lt=self.instance.pk).latest('id')
        if previous.end>data:
            self.add_error('start','Start Date is over previous MOHH end date')
        return data

    def clean_end(self):
        data = self.cleaned_data.get('end')
        previous = Mohh.objects.filter(id__lt=self.instance.pk).latest('id')
        if data and previous.end > data:
            self.add_error('start', 'Start Date is over previous MOHH end date')
        return data

    def clean(self):
        super().clean()
        start=self.cleaned_data.get('start')
        end=self.cleaned_data.get('end')
        if end and end<start:
            raise ValidationError('End Date is earlier than Start Date')

    class Meta:
        model = Mohh
        exclude = ['unit',]