from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserDeleteView, RegisterView, LoginView, AccountEmailActivateView
from . import views

# app_name = 'accounts'


urlpatterns = [
    path('email/confirm/<str:key>', AccountEmailActivateView.as_view(), name='email-activate'),
    path('email/resend-activation/', AccountEmailActivateView.as_view(), name='resend-activation'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]
