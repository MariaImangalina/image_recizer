from django.test import TestCase, Client
from django.core.files import File

from images.forms import ImageUploadForm, ImageResizeForm


class UploadFormTest(TestCase):

    def test_upload_form_url(self):   
        image_test_url = 'https://upload.wikimedia.org/wikipedia/commons/e/e0/JPEG_example_JPG_RIP_050.jpg'
        form_data = {'url_file':image_test_url}
        form = ImageUploadForm(form_data)
        self.assertTrue(form.is_valid())


    def test_upload_form_file(self):
        with open("media/images/test/Slowpoke.jpeg", "rb") as image_test_file:
            form = ImageUploadForm(files={'upload_file':File(image_test_file)})
            self.assertTrue(form.is_valid())
    

    def test_upload_form_empty(self):
        form = ImageUploadForm()
        self.assertFalse(form.is_valid())


    def test_upload_form_both(self):   
        image_test_url = 'https://upload.wikimedia.org/wikipedia/commons/e/e0/JPEG_example_JPG_RIP_050.jpg'
        with open("media/images/test/Slowpoke.jpeg", "rb") as image_test_file:
            form_data = {'url_file':image_test_url}
            form_files = {'upload_file':File(image_test_file)}
            form = ImageUploadForm(data=form_data, files=form_files)
            self.assertFalse(form.is_valid()) 


    def test_upload_form_wrong_format(self):
        with open("media/images/test/wrong.txt", "rb") as test_file:
            form = ImageUploadForm(files={'upload_file':File(test_file)})
            self.assertFalse(form.is_valid())



class ResizeFormTest(TestCase):
    
    def test_resize_empty(self):
        form = ImageResizeForm()
        self.assertFalse(form.is_valid())
        
    def test_resize_wrong(self):
        form_data = {'height':'blah'}
        form = ImageResizeForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_resize_both(self):
        form_data = {'width':500, 'height':400}
        form = ImageResizeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_resize_width(self):
        form_data = {'width':500}
        form = ImageResizeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_resize_height(self):
        form_data = {'height':500}
        form = ImageResizeForm(data=form_data)
        self.assertTrue(form.is_valid())

    
