from django.db import models
from django import forms
import django_filters

from .models import Unit,LIST_CHOICES

class UnitFilter(django_filters.FilterSet):
    def __init__(self,data,*args,**kwargs):
        super().__init__(data,*args,**kwargs)
        data=data.copy()
        data.setdefault('format','paperback')
        data.setdefault('order','-added')

    class Meta:
        model = Unit
        fields = {'code':['exact',],
                  'type':['exact'],
                  }