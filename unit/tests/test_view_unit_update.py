from django.test import TestCase
from django.urls import reverse,resolve
from datetime import date,timedelta

from ..models import Unit
from ..views import UnitUpdate
from ..forms import UnitForm


class Test_View_Update_Unit(TestCase):
    def setUp(self):
        Unit.objects.create(code='abcd', type='d', date_assign=date(2017, 6, 6))
        Unit.objects.create(code='efgh', type='d', date_assign=date(2017, 6, 6))
        self.url = reverse('unitupdate',kwargs={'pk':1})
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_url_resolve_correct_view(self):
        view = resolve('/unit/1/update')
        self.assertEqual(view.func.__name__,UnitUpdate.__name__)

    def test_view_using_correct_template(self):
        self.assertTemplateUsed(self.response,'unit_update.html')

    def test_view_use_correct_form(self):
        form=self.response.context.get('form')
        self.assertIsInstance(form,UnitForm)

    def test_form_use_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')

    def test_success_unit_update_post(self):
        data = {'code':'abcd','type':'d','date_assign':'14/4/2018'}
        response = self.client.post(self.url,data)
        unit_updated=Unit.objects.get(pk=1)
        self.assertEqual(unit_updated.date_assign,date(2018,4,14))
        redirect_url = reverse('unitdetil', kwargs={'pk':unit_updated.pk})
        self.assertRedirects(response,redirect_url)

    def test_empty_field(self):
        data = {'code': '', 'type': '', 'date_assign': ''}
        response = self.client.post(self.url,data)
        form = response.context.get('form')
        self.assertTrue(form.errors)

    def test_unit_code_already_exists(self):
        data = {'code': 'efgh', 'type': 'd', 'date_assign': '14/4/2018'}
        response = self.client.post(self.url,data)
        self.assertFormError(response,'form','code','Unit with this code already exist, please choose another code')

    def test_date_assign_not_yet_happened(self):
        future_date=date.today()+timedelta(1)
        data = {'code': 'qwerty', 'type': 'd', 'date_assign': future_date.strftime('%d/%m/%Y')}
        response = self.client.post(self.url,data)
        today = date.today()
        self.assertFormError(response,'form','date_assign',
                             'This date is not yet happen, max date is {}'.format(today.strftime('%d/%m/%Y')))