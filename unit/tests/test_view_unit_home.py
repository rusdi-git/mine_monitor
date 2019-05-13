from django.test import TestCase
from django.urls import reverse,resolve

from ..views import unit_home

class Test_View_Unit_Home(TestCase):
    def setUp(self):
        url = reverse('unithome')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_url_resolve_correct_view(self):
        view = resolve('/unit/')
        self.assertEqual(view.func.__name__, unit_home.__name__)

    def test_view_using_correct_template(self):
        self.assertTemplateUsed(self.response, 'unit_home.html')