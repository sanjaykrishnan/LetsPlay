from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
               path('contact/', views.ContactView.as_view(), name='contact'),
               path('signup/', views.SignUpView.as_view(), name='signup'),
               path('profile/', views.profile_view, name='profile'),
               path('profile/edit/', views.ProfileUpdate.as_view(),
                    name='edit'),
               path('logout/', views.logout_view, name='logout'),
               path('login/',
                    auth_views.LoginView.as_view(
                        template_name='accounts/login.html'), name='login')
              ]
