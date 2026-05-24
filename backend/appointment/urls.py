from django.urls import path

from . import views

urlpatterns = [
    path('booking/', views.create_appointment_view, name='appointment_booking')
]
