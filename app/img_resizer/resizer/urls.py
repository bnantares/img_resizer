from django.urls import path
from .views import *

urlpatterns = [
    path('', PicturesView.as_view(), name='pictures'),
	path('upload/', PictureAdd.as_view(), name='upload'),
    path('resize/<str:slug>/', PictureResize.as_view(), name='resize'),
]