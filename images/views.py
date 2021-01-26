from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile

import requests
from os import path
from io import BytesIO
from PIL import Image as PIL_Image

from .models import Image
from .forms import ImageUploadForm, ImageResizeForm



class ImageList(ListView):
    context_object_name = 'images'
    queryset = Image.objects.all()



def image_upload_view(request):
    form = ImageUploadForm()

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():

            if 'upload_file' in request.FILES:
                new_image = form.save(commit=False)
                new_image.img = request.FILES['upload_file']
                new_image.name = str(request.FILES['upload_file'])
                new_image.save()

                return redirect("images:resize", pk=new_image.pk)

            else:
                image_url = request.POST['url_file']
                response = requests.get(image_url, stream=True)

                if response.ok and response.headers['content-type'] in ('image/png', 'image/jpeg'):
                    img_temp = NamedTemporaryFile()
                    img_temp.write(response.content)
                    img_temp.flush()

                    new_image = form.save()
                    new_image.name = path.basename(image_url)
                    new_image.img.save(new_image.name, File(img_temp), save=True)

                    return redirect("images:resize", pk=new_image.pk)

                else:
                    messages.info(request, 'Не удалось найти изображение. Попробуйте снова.')

        else:
            print(form.errors)
            
    return render(request, 'images/image_create.html', {'form':form})




def resize_view(request, pk):
    image = Image.objects.get(pk=pk)
    form = ImageResizeForm()
    
    if request.method == 'POST':
        form = ImageResizeForm(request.POST)
                
        if form.is_valid():
            image.pk = None
            image.save()
            with image.img.open() as model_image:
                original_img = PIL_Image.open(model_image)
                width, height = original_img.size

                requested_width = request.POST.get('width')
                requested_height = request.POST.get('height')

                if request.POST.get('width') and request.POST.get('height'):

                    requested_width_float = float(requested_width)
                    requested_height_float = float(requested_height)

                    bigside = width if requested_width_float > requested_height_float else height
                    requested_bigside = requested_width_float if requested_width_float > requested_height_float else requested_height_float

                    coeff = requested_bigside / bigside
                                    
                    
                elif requested_width:
                    coeff = float(requested_width) / width

                elif requested_height:
                    coeff = float(requested_height) / height
            
            
                resized_img = original_img.resize(((int(round(width * coeff))), int(round(height * coeff))), PIL_Image.NEAREST)    
                img_buffer = BytesIO()
                resized_img.save(img_buffer, format=original_img.format, quality=100)

                image.name = str(image.name).split('.')[0] + '_w' + str(resized_img.size[0]) + 'h' + str(resized_img.size[1]) + '.' + original_img.format
                image.img.save(image.name, ContentFile(img_buffer.getvalue()), save=True)
                img_buffer.close()

            return redirect("images:resize", image.pk)
                
    return render(request, 'images/image_resize.html', {'form':form, 'image':image})

