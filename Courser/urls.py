from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.MyProfile.as_view(), name='profile'),
    path('edit/', views.EditBasicInformation.as_view(), name='edit'),
    path('paymentinfo/', views.EditPaymentInformation.as_view(), name='paymentInfo'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),

    path('', views.HomeView.as_view(), name='home'),
    path('category/<int:pk>/', views.CoursesByCategoryListView.as_view(), name='coursesByCategory'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('mycart/', views.MyCart.as_view(), name='myCart'),
    path('payment/', views.Payment.as_view(), name='payment'),

    path('delete/<int:pk>', views.delete_from_cart, name='deleteCourse'),
    path('add/<int:pk>', views.add_to_cart, name='addToCart')
]
