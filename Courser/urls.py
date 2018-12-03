from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.MyProfile.as_view(), name='profile'),
    path('edit/', views.EditProfile.as_view(), name='edit'),
    path('login/', views.Login.as_view(), name='login'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),

    path('', views.HomeView.as_view(), name='home'),
    path('category/<int:pk>/', views.CoursesByCategoryListView.as_view(), name='coursesByCategory'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('addtocart/', views.AddToCartView.as_view(), name='addToCart'),
    path('mycart/', views.MyCart.as_view(), name='myCart'),
    path('payment/', views.Payment.as_view(), name='payment')
]
