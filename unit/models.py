from django.db import models

# Create your models here.
LIST_CHOICES = {'Unit_Type':(('d','DumpTruck'),('e','Excavator'))}

class Unit(models.Model):
    code = models.CharField(max_length=20)
    type = models.CharField(max_length=1, choices=LIST_CHOICES['Unit_Type'])
    date_assign = models.DateField()

    def get_latest_mohh(self):
        try:
            return self.mohh_set.latest('id')
        except models.ObjectDoesNotExist:
            return None




class Mohh(models.Model):
    unit = models.ForeignKey('Unit',on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)