from django.urls import path
from newRango import views

app_name = "newRango"

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    ]
