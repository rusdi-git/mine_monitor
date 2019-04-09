from django.contrib import admin

from .models import Unit,MOHH_Unit,Record_Breakdown_Unit
# Register your models here.

admin.site.register(Unit)
admin.site.register(MOHH_Unit)
admin.site.register(Record_Breakdown_Unit)
