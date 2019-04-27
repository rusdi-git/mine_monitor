# from django.test import TestCase
# from django.urls import reverse,resolve
#
# class GenericTestCase(TestCase):
#     def __init__(self, url='',url_path='',view=None,template=''):
#         super().__init__()
#         self.url = url
#         self.url_path=url_path
#         self.view=view
#         self.template=template
#
#     def setUp(self):
#         self.response = reverse(self.url)
#
#     def test_status_code(self):
#         self.assertEqual(self.response.status_code,200)
#
#     def test_url_path_resolve_correct_view(self):
#         view=resolve(self.url_path)
#         self.assertEqual(view.func.__name__,self.view.__name__)
#
#     def test_view_using_correct_template(self):
#         self.assertTemplateUsed(self.response,self.template)