from django.urls import path

from . import views

urlpatterns = [
    path('appointment/', views.create_appointment_view, name='appointment_booking')
]
