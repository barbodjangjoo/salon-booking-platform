from django.urls import path

from . import views

urlpatterns = [
    path('booking/', views.create_appointment_view, name='appointment_booking'),
    path('me/', views.appointment_list_view, name='appointment_list'),
    
]
