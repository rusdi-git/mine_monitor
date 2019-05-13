from django.test import TestCase
from django.urls import reverse,resolve
from datetime import date,timedelta

from ..models import Unit
from ..views import unit_detil


class Test_View_Unit_Detil(TestCase):
    def setUp(self):
        unit=Unit.objects.create(code='abcd',type='d',date_assign=date(2017,5,5))
        url = reverse('unitdetil',kwargs={'pk':unit.pk})
        self.response=self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_url_resolve_correct_view(self):
        view=resolve('/unit/1')
        self.assertEqual(view.func.__name__,unit_detil.__name__)

    def test_view_using_correct_template(self):
        self.assertTemplateUsed(self.response,'unit_detil.html')