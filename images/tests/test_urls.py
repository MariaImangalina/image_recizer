from django.test import SimpleTestCase
from django.urls import reverse, resolve

from images.views import ImageList, image_upload_view, resize_view
from images.models import Image

class UrlsTest(SimpleTestCase):

    def test_list_url(self):
        url = reverse('images:list')
        self.assertEqual(resolve(url).func.view_class, ImageList)

    def test_new_url(self):
        url = reverse('images:new')
        self.assertEqual(resolve(url).func, image_upload_view)

    def test_resize_url(self):
        url = reverse('images:resize', kwargs={'pk':1})
        self.assertEqual(resolve(url).func, resize_view)        
