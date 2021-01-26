from django.test import TestCase, Client
from django.urls import reverse
from django.core.files import File
from django.test import override_settings

import shutil
import tempfile
from os import path

from images.views import ImageList, image_upload_view, resize_view
from images.models import Image

MEDIA_ROOT=tempfile.mkdtemp()


""" Тестирование стартовой страницы """

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class IndexViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.resize_url = reverse('images:resize', kwargs={'pk':1})
        self.list_url = reverse('images:list')


    def test_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image_list.html')
        self.assertTrue('images' in response.context)
        self.assertContains(response, 'Список изображений')
        self.assertContains(response, 'Добавить изображение')

    def test_list_view_content(self):
        Image.objects.create(name='test_image.jpg', img=File(open('media/images/test/cat_test1.jpg', "rb")))
        Image.objects.create(name='test_image2.jpeg', img=File(open('media/images/test/Slowpoke.jpeg', "rb")))
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.context['images']), 2)


    def tearDown(self):
        print("Deleting temporary files...")
        try:
            shutil.rmtree(MEDIA_ROOT)
        except OSError:
            pass


""" Тестирование загрузки изображений """

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class UploadViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.resize_url = reverse('images:resize', kwargs={'pk':1})
        self.new_url = reverse('images:new')


    def test_upload_image_view_get(self):
        response = self.client.get(self.new_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image_create.html')
        self.assertContains(response, 'Новое изображение')
        self.assertContains(response, 'Отправить')

    def test_upload_image_view_post_url(self):
        image_test_url = 'https://upload.wikimedia.org/wikipedia/commons/e/e0/JPEG_example_JPG_RIP_050.jpg'
        response = self.client.post(self.new_url, {'url_file':image_test_url})
        self.assertRedirects(response, self.resize_url, 302)


    def test_upload_image_view_post_file(self):
        with open("media/images/test/Slowpoke.jpeg", "rb") as image_test_file:
            response = self.client.post(self.new_url, {'upload_file':image_test_file})
            self.assertRedirects(response, self.resize_url, 302)


    def tearDown(self):
        print("Deleting temporary files...")
        try:
            shutil.rmtree(MEDIA_ROOT)
        except OSError:
            pass
    

""" Тестирование изменения размера изображений """

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ResizeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.resize_url = reverse('images:resize', kwargs={'pk':1})
        self.resize_url_result = reverse('images:resize', kwargs={'pk':2})
        with open("media/images/test/Slowpoke.jpeg", "rb") as image_test_file:
            Image.objects.create(name=path.basename(image_test_file.name), img=File(image_test_file))


    def test_resize_image_view_get(self):
        response = self.client.get(self.resize_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/image_resize.html')
        self.assertContains(response, 'Slowpoke.jpeg')


    def test_resize_image_view_post_width(self):
        response = self.client.post(self.resize_url, {'width':200})
        self.assertRedirects(response, self.resize_url_result, 302)

        new_image = Image.objects.get(pk=2)
        self.assertEqual(new_image.img.height, 200)
        self.assertEqual(new_image.img.width, 200)
        self.assertEqual(new_image.name, 'Slowpoke_w200h200.JPEG')


    def test_resize_image_view_post_height(self):
        response = self.client.post(self.resize_url, {'height':300})
        self.assertRedirects(response, self.resize_url_result, 302)

        new_image = Image.objects.get(pk=2)
        self.assertEqual(new_image.img.height, 300)
        self.assertEqual(new_image.img.width, 300)
        self.assertEqual(new_image.name, 'Slowpoke_w300h300.JPEG')


    def test_resize_image_view_post_both(self):
        response = self.client.post(self.resize_url, {'width':500, 'height':400})
        self.assertRedirects(response, self.resize_url_result, 302)

        new_image = Image.objects.get(pk=2)
        self.assertEqual(new_image.img.height, 500)
        self.assertEqual(new_image.img.width, 500)
        self.assertEqual(new_image.name, 'Slowpoke_w500h500.JPEG')


    def test_resize_image_view_post_both2(self):
        response = self.client.post(self.resize_url, {'width':100, 'height':400})
        self.assertRedirects(response, self.resize_url_result, 302)

        new_image = Image.objects.get(pk=2)
        self.assertEqual(new_image.img.height, 400)
        self.assertEqual(new_image.img.width, 400)
        self.assertEqual(new_image.name, 'Slowpoke_w400h400.JPEG')

    
    def tearDown(self):
        print("Deleting temporary files...")
        try:
            shutil.rmtree(MEDIA_ROOT)
        except OSError:
            pass

    

        






    
    

    





        

    



    
