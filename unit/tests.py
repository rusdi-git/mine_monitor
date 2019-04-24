from django.test import TestCase
from django.urls import reverse,resolve
from datetime import date

from .models import Unit
from .views import home, UnitNew
from .form import UnitForm

# Create your tests here.
class Test_View_Home(TestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_url_resolve_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func,home)

    def test_view_using_correct_template(self):
        self.assertTemplateUsed(self.response,'home.html')


class Test_View_New_Unit(TestCase):
    def setUp(self):
        Unit.objects.create(code='abcd',type='d',date_assign=date(2017,6,6))
        self.url = reverse('unitnew')
        self.get = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.get.status_code,200)

    def test_url_resolve_unit_new_view(self):
        view = resolve('/unit/new')
        self.assertEqual(view.func.__name__,UnitNew.__name__)

    def view_using_correct_template(self):
        self.assertTemplateUsed(self.get,'unit_new.html')

    def test_view_use_correct_form(self):
        form=self.get.context.get('form')
        self.assertIsInstance(form,UnitForm)

    def test_use_csrf(self):
        self.assertContains(self.get,'csrfmiddlewaretoken')

    def test_success_unit_new_post(self):
        data = {'code':'qwerty','type':'d','date_assign':'14/4/2018'}
        response = self.client.post(self.url,data)
        self.assertTrue(Unit.objects.filter(code='qwerty').exists())
        redirect_url = reverse('home')
        self.assertRedirects(response,redirect_url)

    def test_empty_field(self):
        data = {'code': '', 'type': '', 'date_assign': ''}
        response = self.client.post(self.url,data)
        form = response.context.get('form')
        self.assertTrue(form.errors)

    def test_unit_code_already_exists(self):
        data = {'code': 'abcd', 'type': 'd', 'date_assign': '14/4/2018'}
        response = self.client.post(self.url,data)
        self.assertFormError(response,'form','code','Unit with this code already exist, please choose another code')

    def test_date_assign_not_yet_happened(self):
        data = {'code': 'qwerty', 'type': 'd', 'date_assign': '14/4/2020'}
        response = self.client.post(self.url,data)
        today = date.today()
        self.assertFormError(response,'form','date_assign',
                             'This date is not yet happen, max date is {}'.format(today.strftime('%d/%m/%Y')))