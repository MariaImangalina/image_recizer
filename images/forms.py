from django import forms

from os import path

from .models import Image


class ImageUploadForm(forms.ModelForm):
    url_file = forms.URLField(max_length=500, required=False, label='Ссылка')
    upload_file = forms.ImageField(required=False, label='Файл')

    class Meta:
        model = Image
        fields = ('url_file', 'upload_file')

    def clean(self):
        cleaned_data=super(ImageUploadForm, self).clean()
        url_file = cleaned_data.get('url_file')
        upload_file = cleaned_data.get('upload_file')

        if not url_file and not upload_file:
            raise forms.ValidationError('Для продолжения необходимо заполнить хотя бы одно поле')
        elif url_file and upload_file:
            raise forms.ValidationError('Пожалуйста, выберите только один из методов загрузки')
        
        return cleaned_data




class ImageResizeForm(forms.Form):
    width = forms.IntegerField(required=False, label='Ширина')
    height = forms.IntegerField(required=False, label='Высота')

    def clean(self):
        cleaned_data=super(ImageResizeForm, self).clean()
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')

        if not width and not height:
            raise forms.ValidationError('Для продолжения необходимо заполнить хотя бы одно поле')

        return cleaned_data