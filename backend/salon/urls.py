from django.urls import path

from . import views

urlpatterns = [
    path("category/", views.category_list_view, name="category_list"),
    path("category/<int:pk>/", views.category_detail_view, name="category_detail"),
    path("service/", views.service_list_view, name='service_list'),
    path('service/<int:pk>/', views.service_detail_view, name='service_detail'),
    path('staff/', views.staff_list_view, name='staff_list'),
    

    # path("service/<int:pk>/", views.service_list_view, name="service_list"),
    # path("staff/<int:pk>/slots/", views.staff_list_view, name="staff_slots_list"),
    # path('appointment/', views.appointment_list_view, name='appointment_list'),
    # path('appointment/<int:pk>/', views.appointment_detail_view, name= 'appointment_detail'),
    # path('appointment/new/', views.appointment_create_view, name='create_appointment'),
]
