from django.db import models

# Create your models here.


class Record_Breakdown_Unit(models.Model):
    unit = models.ForeignKey('unit.Mohh', on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    description = models.TextField(max_length=500)