from django.urls import path, include
from . import views

app_name = 'images'

urlpatterns = [
    path('', views.ImageList.as_view(), name = 'list'),
    path('new/', views.image_upload_view, name='new'),
    path('detail/<int:pk>/', views.resize_view, name='resize'),
]