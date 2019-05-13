from django.test import TestCase
from django.urls import reverse,resolve
from datetime import date

from ..models import Unit
from ..views import unit_query


class Test_View_Query_Unit(TestCase):
    def setUp(self):
        Unit.objects.create(code='abcd', type='d', date_assign=date(2017, 6, 6))
        Unit.objects.create(code='efgh', type='d', date_assign=date(2017, 6, 6))
        Unit.objects.create(code='asdq', type='e', date_assign=date(2017, 6, 6))
        self.url = reverse('unitquery')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_url_resolve_correct_view(self):
        view = resolve('/unit/query')
        self.assertEqual(view.func.__name__,unit_query.__name__)

    def view_using_correct_template(self):
        self.assertTemplateUsed(self.response,'unit_query.html')

    def test_parameter_query_result_correct_data(self):
        # url = resolve('/unit/query?type=d')
        # url = reverse('unitquery',kwargs={'type':'d'})
        url ='{}?type=d'.format(reverse(unit_query))
        response = self.client.get(url)
        self.assertNotContains(response,'asdq')
        self.assertContains(response,'abcd')