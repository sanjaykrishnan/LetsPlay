from django.urls import path

from . import views

app_name = 'sports_centre'

urlpatterns = [
               path('sports-centre/create/',
                    views.CreateGroundView.as_view(), name='create'),
               path('', views.HomeView.as_view(), name='home'),
               path('sports-centre/<int:pk>/',
                    views.SportsCentreDetailView.as_view(), name='detail'),
               path('sports-centre/<int:pk>/edit/',
                    views.EditGroundView.as_view(), name='edit'),
               path('sports-centre/<int:pk>/delete/',
                    views.DeleteGroundView.as_view(), name='delete'),
               path('sports-centre/<int:pk>/book/',
                    views.BookingView.as_view(), name='book'),
               path('sports-centre/booking-list/',
                    views.BookingListing.as_view(), name='booking-list'),
              ]
