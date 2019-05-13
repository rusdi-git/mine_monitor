from django.test import TestCase
from django.urls import reverse,resolve

from ..views import home

class Test_View_Home(TestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_url_resolve_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__,home.__name__)

    def test_view_using_correct_template(self):
        self.assertTemplateUsed(self.response,'home.html')