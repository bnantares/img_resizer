from django import forms
from .models import Picture
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

"""Форма для загрузки картинки"""
class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = ['picture_url', 'img']
    def clean(self):
        picture_url = self.cleaned_data.get('picture_url')
        img = self.cleaned_data.get('img')
        if picture_url == "" and img is None:
            raise forms.ValidationError(_('Укажите ссылку или загрузите файл изображения!'), code='invalid')
        if picture_url is not "" and img is not None:
            raise forms.ValidationError(_('Выберите только одно поле!'), code='invalid')

"""Форма для изменения картинки"""
class ResizeForm(forms.Form):
    picture_resize_height = forms.IntegerField(label='Выоста, пиксели', required=False, help_text="(Максимум 1080 пикселей)")
    picture_resize_width = forms.IntegerField(label='Ширина, пиксели', required=False, help_text="(Максимум 1920 пикселей)")

    def clean(self):
        width = self.cleaned_data.get('picture_resize_width')
        height = self.cleaned_data.get('picture_resize_height')
        if width is None and height is None:
            raise forms.ValidationError(_('Заполните хотя бы одно поле'), code='invalid')
    