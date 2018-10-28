from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.MyProfile.as_view(), name='profile'),
    path('edit/', views.EditProfile.as_view(), name='edit')
]
