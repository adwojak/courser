from django.urls import path
from . import views

app_name = 'Courser'
urlpatterns = [
    path('', views.index, name='index'),
]
