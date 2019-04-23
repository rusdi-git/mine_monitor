from django.test import TestCase
from django.urls import reverse,resolve

from .views import home
# Create your tests here.
class test_view_home(TestCase):
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