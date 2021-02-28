from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Picture
from .forms import PictureForm, ResizeForm
from PIL import Image
from urllib.request import urlopen
from django.conf import settings
import tempfile


class PicturesView(View):
    """Список изображений"""
    def get(self, request):
        pictures = Picture.objects.all()
        return render(request, "resizer/pictures_list.html", {"pictures": pictures})


class PictureAdd(View):
    """Добавляем картинку"""
    def get(self, request):
        form = PictureForm(request.GET)
        return render(request, 'resizer/upload.html', context={"form": form})
    
    def post(self, request):
        bound_form = PictureForm(request.POST, request.FILES)
        if bound_form.is_valid():
            if 'img' in request.FILES:
                bound_form.img = request.FILES['img']
            bound_form.save()
            return redirect('pictures')
        else:
            return render(request, 'resizer/upload.html', context={"form": bound_form})


class PictureResize(View):
    """Изменяем картинку"""
    def get(self, request, slug):
        form = ResizeForm(request.GET)
        pictures = Picture.objects.get(slug__iexact=slug)
        return render(request, 'resizer/resize.html', {"pictures": pictures, "form": form})

    def post(self, request, slug):
        form = ResizeForm(request.POST)
        picture = Picture.objects.get(slug__iexact=slug)
        url = picture.picture_url
        if (url == ""):
            fpath = str(settings.BASE_DIR) + "/media/" + picture.img.name
            new_image = Image.open(fpath)
        else:
            new_image = Image.open(urlopen(url))
        if new_image.mode in ("RGBA", "P"):
            new_image = new_image.convert("RGB")
        width, height = new_image.size
        new_width = request.POST['picture_resize_width']
        new_height = request.POST['picture_resize_height']
        if new_width == '':
            new_width = width
        if new_height == '':
            new_height = height
        new_image.thumbnail((int(new_width), int(new_height)), Image.ANTIALIAS)
        temp_fname = next(tempfile._get_candidate_names()) + ".jpg"
        url_resized = str(settings.BASE_DIR) + "/media/images/temp/" + temp_fname
        new_image.save(url_resized, 'JPEG')
        return render(request, 'resizer/resize.html', {"temp_fname": temp_fname, "form": form})
            


