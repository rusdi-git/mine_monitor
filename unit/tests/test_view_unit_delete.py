from django.test import TestCase
from django.urls import reverse,resolve
from datetime import date

from ..models import Unit
from ..views import UnitDelete

class Test_View_Delete_Unit(TestCase):
    def setUp(self):
        Unit.objects.create(code='abcd', type='d', date_assign=date(2017, 6, 6))
        Unit.objects.create(code='efgh', type='d', date_assign=date(2017, 6, 6))
        self.url = reverse('unitdelete', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_url_resolve_correct_view(self):
        view = resolve('/unit/1/delete')
        self.assertEqual(view.func.__name__,UnitDelete.__name__)

    def test_view_using_correct_template(self):
        self.assertTemplateUsed(self.response,'unit_delete.html')

    def test_form_use_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')

    def test_success_unit_delete_post(self):
        self.assertTrue(Unit.objects.filter(pk=1).exists())
        response = self.client.post(self.url)
        self.assertFalse(Unit.objects.filter(pk=1).exists())
        redirect_url = reverse('unithome')
        self.assertRedirects(response,redirect_url)